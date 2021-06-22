from app import app, db
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    send_file,
    send_from_directory,
    safe_join,
    abort,
)
from flask_login import login_required, current_user
from app.models.tables import (
    Pessoa,
    Processo,
    Contribuinte,
    Status,
    Servidor,
    ArquivoProcesso,
    Atualizacao,
    Terreno,
)
from datetime import datetime
from werkzeug.utils import secure_filename
import os, uuid, sys


def gerar_nome_arquivo(arquivo):
    extensaoArquivo = arquivo.filename.split(".")
    extensaoArquivo = extensaoArquivo[len(extensaoArquivo) - 1]
    arquivo.filename = str(uuid.uuid4()) + "." + extensaoArquivo
    return arquivo


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        pesquisa = request.form["inputSearch"]

        subquery = (
            db.session.query(
                db.func.max(Atualizacao.id).label("max_id"),
                Atualizacao.processo_id,
                Atualizacao.status_id,
            )
            .group_by(Atualizacao.processo_id)
            .subquery()
        )

        query = (
            db.session.query(Atualizacao, Processo, Status)
            .join(
                subquery,
                Atualizacao.id == subquery.c.max_id,
            )
            .join(Processo, Processo.id == Atualizacao.processo_id)
            .join(Status, Status.id == Atualizacao.status_id)
            .filter(Processo.numero == pesquisa)
            .order_by(Status.id)
            .all()
        )
        if not query:
            mensagem = "Não há processos correspondentes com a pesquisa"
            return render_template("index.html", mensagem=mensagem)

        return render_template("index.html", query=query)


@app.route("/novo_processo", methods=["GET", "POST"])
@login_required
def cadastrar_processos():
    if request.method == "GET":
        return render_template("cadastro_processo.html")

    if request.method == "POST":

        contribuinte = Contribuinte.query.filter(
            Contribuinte.pessoa_id.like(current_user.id)
        ).first()

        if contribuinte:

            nome = request.form["inputName"]
            tipo_processo = request.form["inputKind"]
            tipo_lote = request.form["inputType"]
            data_inicio = datetime.now()

            rua = request.form["inputRua"]
            numero = request.form["inputNumber"]
            bairro = request.form["inputBairro"]
            lote = request.form["inputLote"]
            quadra = request.form["inputQuadra"]
            setor = request.form["inputSetor"]
            if (
                (not tipo_processo)
                or (not tipo_lote)
                or (not rua)
                or (not numero)
                or (not bairro)
                or (not lote)
                or (not quadra)
                or (not setor)
            ):
                mensagem = "Os campos marcados com '*' são obrigatórios"
                return render_template("cadastro_processo.html", mensagem=mensagem)

            terreno = Terreno(
                lote=lote,
                quadra=quadra,
                setor=setor,
                rua=rua,
                bairro=bairro,
                numero=numero,
            )
            db.session.add(terreno)
            db.session.commit()

            app.logger.info(
                "O seguinte usuário tentou criar um processo " + str(contribuinte.id)
            )

            processo = Processo(
                nome=nome,
                tipo_processo=tipo_processo,
                tipo_lote=tipo_lote,
                data_inicio=data_inicio,
                contribuinte_id=contribuinte.id,
                terreno_id=terreno.id,
                servidor_id=1,
            )
            db.session.add(processo)
            db.session.commit()

            id = str(processo.id)

            processo.numero = f"{id.zfill(4)}/{data_inicio.year}"
            db.session.commit()

            pastaNova = "./app/uploads/" + str(processo.id)
            os.makedirs(pastaNova)

            arquivoRequerimento = request.files["inputRequerimento"]
            if arquivoRequerimento:
                gerar_nome_arquivo(arquivoRequerimento)
                arquivoRequerimento.save(
                    os.path.join(
                        pastaNova, secure_filename(arquivoRequerimento.filename)
                    )
                )

            arquivoRG = request.files["inputCopiaRG"]
            if arquivoRG:
                gerar_nome_arquivo(arquivoRG)
                arquivoRG.save(
                    os.path.join(pastaNova, secure_filename(arquivoRG.filename))
                )

            arquivoCPF = request.files["inputCopiaCPF"]
            if arquivoCPF:
                gerar_nome_arquivo(arquivoCPF)
                arquivoCPF.save(
                    os.path.join(pastaNova, secure_filename(arquivoCPF.filename))
                )

            arquivoCertPref = request.files["inputCertidaoPrefeitura"]
            if arquivoCertPref:
                gerar_nome_arquivo(arquivoCertPref)
                arquivoCertPref.save(
                    os.path.join(pastaNova, secure_filename(arquivoCertPref.filename))
                )

            arquivoCertSAAE = request.files["inputCertidaoSAAE"]
            if arquivoCertSAAE:
                gerar_nome_arquivo(arquivoCertSAAE)
                arquivoCertSAAE.save(
                    os.path.join(pastaNova, secure_filename(arquivoCertSAAE.filename))
                )

            arquivoTitulo = request.files["inputTituloImovel"]
            if arquivoTitulo:
                gerar_nome_arquivo(arquivoTitulo)
                arquivoTitulo.save(
                    os.path.join(pastaNova, secure_filename(arquivoTitulo.filename))
                )

            arquivoComprovanteRest = request.files["inputComprovanteResidencia"]
            if arquivoComprovanteRest:
                gerar_nome_arquivo(arquivoComprovanteRest)
                arquivoComprovanteRest.save(
                    os.path.join(
                        pastaNova, secure_filename(arquivoComprovanteRest.filename)
                    )
                )

            arquivoAnalise = request.files["inputFileAnalises"]
            if arquivoAnalise:
                gerar_nome_arquivo(arquivoAnalise)
                arquivoAnalise.save(
                    os.path.join(pastaNova, secure_filename(arquivoAnalise.filename))
                )

            atualizacao = Atualizacao(
                data_atualizacao=datetime.now(), status_id=1, processo_id=processo.id
            )

            a1 = ArquivoProcesso(
                requerimento=arquivoRequerimento.filename,
                copiaRG=arquivoRG.filename,
                certidaoNegativaPrefeitura=arquivoCertPref.filename,
                certidaoNegativaSAAE=arquivoCertSAAE.filename,
                tituloImovel=arquivoTitulo.filename,
                copiaCPF=arquivoCPF.filename,
                copiaComprovanteResidencia=arquivoComprovanteRest.filename,
                projetoArt=arquivoAnalise.filename,
                processo_id=processo.id,
            )

            db.session.add(a1)
            db.session.add(atualizacao)
            db.session.commit()

        else:
            mensagem = (
                "Você não está cadastrado como contribuinte para cadastrar processos"
            )

            return render_template("home.html", mensagem=mensagem)

    return redirect("/home")


@app.route("/processo/<id_processo>/arquivos/<arquivo>")
def enviaArquivos(id_processo, arquivo):
    pasta = "./" + os.sep + "uploads" + os.sep + id_processo + os.sep + arquivo
    return send_file(pasta, as_attachment=False)


@app.route("/alterar_processo/<id_processo>", methods=["POST"])
@login_required
def alterar_processo(id_processo):
    nome = request.form["inputName"]
    processo = Processo.query.filter_by(id=id_processo).first()
    if processo.nome != nome:
        processo.nome = nome
        db.session.commit()
    subquery = (
        db.session.query(
            db.func.max(Atualizacao.id).label("max_id"),
            Atualizacao.processo_id,
            Atualizacao.status_id,
        )
        .group_by(Atualizacao.processo_id)
        .subquery()
    )

    query = (
        db.session.query(Atualizacao, Processo, Status)
        .join(
            subquery,
            Atualizacao.id == subquery.c.max_id,
        )
        .join(Processo, Processo.id == Atualizacao.processo_id)
        .join(Status, Status.id == Atualizacao.status_id)
        .filter(Processo.id == processo.id)
        .filter((Status.nome == "Aprovado") | (Status.nome == "Não aprovado"))
        .order_by(Status.id)
        .all()
    )

    if not query:
        pastaNova = "./app/uploads/" + str(processo.id)

        arquivoRequerimento = request.files["inputRequerimento"]
        if arquivoRequerimento:
            gerar_nome_arquivo(arquivoRequerimento)
            arquivoRequerimento.save(
                os.path.join(pastaNova, secure_filename(arquivoRequerimento.filename))
            )

        arquivoRG = request.files["inputCopiaRG"]
        if arquivoRG:
            gerar_nome_arquivo(arquivoRG)
            arquivoRG.save(os.path.join(pastaNova, secure_filename(arquivoRG.filename)))

        arquivoCPF = request.files["inputCopiaCPF"]
        if arquivoCPF:
            gerar_nome_arquivo(arquivoCPF)
            arquivoCPF.save(
                os.path.join(pastaNova, secure_filename(arquivoCPF.filename))
            )

        arquivoCertPref = request.files["inputCertidaoPrefeitura"]
        if arquivoCertPref:
            gerar_nome_arquivo(arquivoCertPref)
            arquivoCertPref.save(
                os.path.join(pastaNova, secure_filename(arquivoCertPref.filename))
            )

        arquivoCertSAAE = request.files["inputCertidaoSAAE"]
        if arquivoCertSAAE:
            gerar_nome_arquivo(arquivoCertSAAE)
            arquivoCertSAAE.save(
                os.path.join(pastaNova, secure_filename(arquivoCertSAAE.filename))
            )

        arquivoTitulo = request.files["inputTituloImovel"]
        if arquivoTitulo:
            gerar_nome_arquivo(arquivoTitulo)
            arquivoTitulo.save(
                os.path.join(pastaNova, secure_filename(arquivoTitulo.filename))
            )

        arquivoComprovanteRest = request.files["inputComprovanteResidencia"]
        if arquivoComprovanteRest:
            gerar_nome_arquivo(arquivoComprovanteRest)
            arquivoComprovanteRest.save(
                os.path.join(
                    pastaNova, secure_filename(arquivoComprovanteRest.filename)
                )
            )

        arquivoAnalise = request.files["inputFileAnalises"]
        if arquivoAnalise:
            gerar_nome_arquivo(arquivoAnalise)
            arquivoAnalise.save(
                os.path.join(pastaNova, secure_filename(arquivoAnalise.filename))
            )

        arquivos = ArquivoProcesso.query.filter_by(processo_id=id_processo).first()
        if arquivoRequerimento.filename:
            arquivos.requerimento = (arquivoRequerimento.filename,)
        if arquivoRG.filename:
            arquivos.copiaRG = (arquivoRG.filename,)
        if arquivoCertPref.filename:
            arquivos.certidaoNegativaPrefeitura = (arquivoCertPref.filename,)
        if arquivoCertSAAE.filename:
            arquivos.certidaoNegativaSAAE = (arquivoCertSAAE.filename,)
        if arquivoTitulo.filename:
            arquivos.tituloImovel = (arquivoTitulo.filename,)
        if arquivoCPF.filename:
            arquivos.copiaCPF = (arquivoCPF.filename,)
        if arquivoComprovanteRest.filename:
            arquivos.copiaComprovanteResidencia = (arquivoComprovanteRest.filename,)
        if arquivoAnalise.filename:
            arquivos.projetoArt = (arquivoAnalise.filename,)

        data = datetime.now()
        atualizacao = Atualizacao(
            data_atualizacao=data,
            status_id=1,
            processo_id=id_processo,
        )
        db.session.add(atualizacao)

        processo.parecer = ""

        db.session.commit()
        return redirect("/home")
    else:
        mensagem = "Não é possível aterar este processo"
        return render_template("erro.html", mensagem=mensagem)


@app.route("/alterar_nome_processo/<id_processo>", methods=["POST"])
@login_required
def alterar_nome_processo(id_processo):
    nome = request.form["inputName"]
    processo = Processo.query.filter_by(id=id_processo).first()
    if processo.nome != nome:
        processo.nome = nome
        db.session.commit()
        return redirect("/home")


@app.route("/processo/<id_processo>")
def visualizar_processo(id_processo):
    processo = Processo.query.filter_by(id=id_processo).first()
    arquivos = os.listdir("./app/uploads/" + id_processo + "/")

    id_terreno = processo.terreno_id

    atualizacoes = Atualizacao.query.filter_by(processo_id=id_processo).first()
    status = Status.query.filter_by(id=atualizacoes.id).first()
    arquivo = ArquivoProcesso.query.filter_by(processo_id=id_processo).first()
    terreno = Terreno.query.filter_by(id=processo.terreno_id).first()

    return render_template(
        "processo.html",
        processo=processo,
        arquivos=arquivos,
        id_processo=id_processo,
        status=status,
        arquivo=arquivo,
        terreno=terreno,
    )


@app.route("/analise_processo", methods=["GET", "POST"])
@login_required
def analisar_processos():

    usuario = current_user.get_id()
    servidor = Servidor.query.filter(Servidor.pessoa_id.like(usuario)).first()

    if servidor:
        id_servidor = servidor.id
        app.logger.info(
            "O seguinte usuário tentou mostrar seus processos: " + str(id_servidor)
        )

        subquery = (
            db.session.query(
                db.func.max(Atualizacao.id).label("max_id"),
                Atualizacao.processo_id,
                Atualizacao.status_id,
            )
            .group_by(Atualizacao.processo_id)
            .subquery()
        )

        processos = (
            db.session.query(Atualizacao, Processo, Status)
            .join(
                subquery,
                Atualizacao.id == subquery.c.max_id,
            )
            .join(Processo, Processo.id == Atualizacao.processo_id)
            .join(Status, Status.id == Atualizacao.status_id)
            .filter((Status.nome == "Encaminhado") | (Status.nome == "Em análise"))
            .order_by(Status.id)
            .all()
        )
        return render_template("lista_processo.html", processos=processos)
    else:
        mensagem = "Você não está autorizado a ver esta página"

    return render_template("lista_processo.html", mensagem=mensagem)


@app.route("/analise_processo/<id_processo>", methods=["GET", "POST"])
@login_required
def analise_de_processo(id_processo):
    processo = Processo.query.filter_by(id=id_processo).first()
    arquivos = os.listdir("./app/uploads/" + id_processo + "/")
    analise = 1
    atualizacoes = Atualizacao.query.filter_by(processo_id=id_processo).first()
    status = Status.query.filter_by(id=atualizacoes.id).first()
    arquivo = ArquivoProcesso.query.filter_by(processo_id=id_processo).first()
    terreno = Terreno.query.filter_by(id=processo.terreno_id).first()
    if request.method == "GET":
        return render_template(
            "analise_processo.html",
            processo=processo,
            arquivos=arquivos,
            arquivo=arquivo,
            analise=analise,
            id_processo=id_processo,
            status=status,
            terreno=terreno,
        )

    if request.method == "POST":
        teste = request.form.getlist("aaa")
        processo = Processo.query.filter_by(id=id_processo).first()
        if len(teste) == 5:
            status = 3

            data = datetime.now()
            atualizacao = Atualizacao(
                data_atualizacao=data,
                status_id=status,
                processo_id=id_processo,
            )
            db.session.add(atualizacao)
            processo.parecer = ""
            processo.atualizacao_id = atualizacao.id
            db.session.commit()

        else:
            if request.form["inputParecer"]:
                status = 5
                data = datetime.now()
                atualizacao = Atualizacao(
                    data_atualizacao=data,
                    status_id=status,
                    processo_id=id_processo,
                )
                db.session.add(atualizacao)
                processo.parecer = request.form["inputParecer"]
                db.session.commit()

            else:
                mensagem = (
                    "Você precisa informar o motivo de estar devolvendo o processo"
                )
                return render_template(
                    "analise_processo.html",
                    processo=processo,
                    arquivos=arquivos,
                    arquivo=arquivo,
                    analise=analise,
                    id_processo=id_processo,
                    status=status,
                    terreno=terreno,
                    mensagem=mensagem,
                )

        return redirect("/analise_processo")


@app.route("/processo/<processo_id>/recusar")
@login_required
def recusar_processo(processo_id):
    processo = Processo.query.filter_by(id=processo_id).first()

    data = datetime.now()
    atualizacao = Atualizacao(
        data_atualizacao=data,
        status_id=4,
        processo_id=processo.id,
    )
    db.session.add(atualizacao)
    processo.parecer = ""
    db.session.commit()
    return redirect("/analise_processo")
