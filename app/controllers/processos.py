from app import app, db
from flask import render_template, redirect, request
from flask_login import login_required, current_user
from app.models.tables import (
    Pessoa,
    Processo,
    Contribuinte,
    Status,
    Servidor,
    ArquivoProcesso,
    CheckList,
    Atualizacao,
)
from datetime import datetime
import os, uuid


@app.route("/novo_processo", methods=["GET", "POST"])
@login_required
def cadastrar_processos():
    if request.method == "GET":
        return render_template("cadastro_processo.html")

    if request.method == "POST":

        nome = request.form["inputName"]
        numero = request.form["inputNumber"]
        tipo_processo = request.form["inputKind"]
        tipo_lote = request.form["inputType"]
        data_inicio = datetime.now()
        copiaRG = request.files["inputCopiaRG"]
        fileName = str(uuid.uuid4())

        contribuinte_id = current_user.get_id()
        # Contribuinte.query.filter_by(pessoa_id=contribuinte_id).first()
        contribuinte = Contribuinte.query.filter(
            Contribuinte.pessoa_id.like(contribuinte_id)
        ).first()

        app.logger.info(
            "O seguinte usuário tentou criar um processo " + str(contribuinte_id)
        )

        # filename = str(uuid.uuid4())
        # filename = filename+".pdf"
        processo = Processo(
            nome=nome,
            numero=numero,
            tipo_processo=tipo_processo,
            tipo_lote=tipo_lote,
            data_inicio=data_inicio,
            contribuinte_id=contribuinte.id,
            servidor_id=1,
        )
        db.session.add(processo)
        db.session.commit()

        atualizacao = Atualizacao(
            data_atualizacao=datetime.now(), status_id=1, processo_id=processo.id
        )

        arquivo = ArquivoProcesso(
            copiaRG=fileName,
            processo_id=processo.id,
        )

        checklist = CheckList(
            processo_id=processo.id,
        )

        pastaNova = "./app/uploads/" + str(processo.id)
        os.makedirs(pastaNova)

        copiaRG.save(
            os.path.join(app.config["UPLOAD_FOLDER"] + "/" + str(processo.id), fileName)
        )

        db.session.add(arquivo)
        db.session.add(checklist)
        db.session.add(atualizacao)
        db.session.commit()

    return redirect("/home")


@app.route("/alterar_processo/<id_processo>", methods=["POST"])
@login_required
def alterar_processo(id_processo):
    nome = request.form["inputName"]
    processo = Processo.query.filter_by(id=id_processo).first()
    processo.nome = nome
    db.session.commit()
    return redirect("/home")


@app.route("/processo/<id_processo>")
def visualizar_processo(id_processo):
    processo = Processo.query.filter_by(id=id_processo).first()
    arquivo = ArquivoProcesso.query.filter_by(processo_id=id_processo).first()

    return render_template("processo.html", processo=processo, arquivo=arquivo)


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

        processos = Processo.query.filter(Processo.servidor_id.like(id_servidor)).all()
        return render_template("lista_processo.html", processos=processos)
    else:
        mensagem = "Você não está autorizado a ver esta página"

    return render_template("lista_processo.html", mensagem=mensagem)


@app.route("/analise_processo/<id_processo>", methods=["GET", "POST"])
@login_required
def analise_de_processo(id_processo):
    processo = Processo.query.filter_by(id=id_processo).first()
    arquivo = ArquivoProcesso.query.filter_by(processo_id=id_processo).first()
    analise = 1
    return render_template(
        "processo.html", processo=processo, arquivo=arquivo, analise=analise
    )


@app.route("/processo_analisado/<id_processo>/<status>", methods=["GET", "POST"])
@login_required
def processo_analisado(id_processo, status):
    # checkBoxRequerimento = request.form["checkBoxRequerimento"]
    checkBoxRequerimento = True
    checklist = CheckList.query.filter_by(processo_id=id_processo).first()

    data_inicio = datetime.now()
    atualizacao = Atualizacao(
        data_atualizacao=data_inicio,
        status_id=status,
    )
    db.session.add(atualizacao)

    processo = Processo.query.filter_by(id=id_processo).first()
    processo.atualizacao_id = atualizacao.id
    checklist.requerimento = checkBoxRequerimento

    db.session.commit()

    return redirect("/analise_processo")
