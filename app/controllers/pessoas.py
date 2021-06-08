from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from sqlalchemy import func
import sys, uuid
from app.models.tables import (
    Pessoa,
    Processo,
    Contribuinte,
    Servidor,
    Atualizacao,
    Status,
)
from datetime import datetime
import bcrypt


@login_manager.user_loader
def get_pessoa(pessoa_id):
    return Pessoa.query.filter_by(id=pessoa_id).first()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("login.html", mensagem=mensagem)

    if request.method == "POST":
        email = request.form["inputEmail"]
        senha = request.form["inputPassword"]

        pessoa = Pessoa.query.filter_by(email=email).first()
        auth = False

        if pessoa:
            auth = bcrypt.checkpw(senha.encode("utf-8"), pessoa.senha.encode("utf-8"))
        if not pessoa or not auth:
            mensagem = "E-mail ou senha inválidos"
            return render_template("login.html", mensagem=mensagem)
        else:
            login_user(pessoa)
            usuario = pessoa.id
            servidor = Servidor.query.filter(Servidor.pessoa_id.like(usuario)).first()
            contribuinte = Contribuinte.query.filter(
                Contribuinte.pessoa_id.like(usuario)
            ).first()
            if servidor:
                return redirect("/analise_processo")
            if contribuinte:
                return redirect("/home")
            else:
                return redirect("/home")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("cadastro.html")

    if request.method == "POST":
        nome = request.form["inputName"]
        cpf = request.form["inputCPF"]
        email = request.form["inputEmail"]
        if request.form["inputPassword"] == request.form["inputPasswordConfirm"]:
            senha = request.form["inputPassword"]
        else:
            mensagem = "As senhas não correspondem"
            return render_template("cadastro.html", mensagem=mensagem)
        senhaEcriptada = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())
        contato = request.form["inputPhone"]
        data_cadastro = datetime.now()

        pessoa = Pessoa(
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senhaEcriptada,
            contato=contato,
            data_cadastro=data_cadastro,
        )
        db.session.add(pessoa)
        db.session.commit()

        contribuinte = Contribuinte(cpf=pessoa.cpf, pessoa_id=pessoa.id)
        db.session.add(contribuinte)
        db.session.commit()

    return redirect("/login")


@app.route("/cadastro_servidor", methods=["GET", "POST"])
@login_required
def cadastro_servidor():
    if request.method == "GET":
        mensagem = request.args.get("mensagem")
        return render_template("cadastro_servidor.html")

    if request.method == "POST":
        nome = request.form["inputName"]
        cpf = request.form["inputCPF"]
        email = request.form["inputEmail"]
        if request.form["inputPassword"] == request.form["inputPasswordConfirm"]:
            senha = request.form["inputPassword"]
        else:
            mensagem = "As senhas não correspondem"
            return render_template("cadastro_servidor.html", mensagem=mensagem)
        senhaEcriptada = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())
        contato = request.form["inputPhone"]
        matricula = request.form["inputMatricula"]
        data_cadastro = datetime.now()

        servidor_id = request.form["getUserID"]
        servidor_admin = Servidor.query.filter(
            Servidor.pessoa_id.like(servidor_id)
        ).first()

        if servidor_admin.admin == True:
            pessoa = Pessoa(
                nome=nome,
                cpf=cpf,
                email=email,
                senha=senhaEcriptada,
                contato=contato,
                data_cadastro=data_cadastro,
            )
            db.session.add(pessoa)
            db.session.commit()

            servidor = Servidor(
                matricula=matricula,
                pessoa_id=pessoa.id,
                admin=False,
            )
            db.session.add(servidor)
            db.session.commit()

        if servidor_admin.admin == False:
            mensagem = "Usuário não autorizado para cadastrar um Servidor"
            return render_template("cadastro_servidor.html", mensagem=mensagem)

    return redirect("/home")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@login_manager.unauthorized_handler
def nao_autorizado():
    return redirect(
        url_for("login", mensagem="Este recurso estará disponível após o login")
    )


@app.route("/home")
@login_required
def listarProcessos():

    usuario = current_user.get_id()
    contribuinte = Contribuinte.query.filter(
        Contribuinte.pessoa_id.like(usuario)
    ).first()

    if contribuinte:

        id_contribuinte = contribuinte.id
        app.logger.info(
            "O seguinte usuário tentou mostrar seus processos: " + str(id_contribuinte)
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

        query = (
            db.session.query(Atualizacao, Processo, Status)
            .join(
                subquery,
                Atualizacao.id == subquery.c.max_id,
            )
            .join(Processo, Processo.id == Atualizacao.processo_id)
            .join(Status, Status.id == Atualizacao.status_id)
            .all()
        )

        if query:
            return render_template("home.html", query=query)
        else:
            mensagem = (
                "Você ainda não abriu nenhum processo. Clique no botão para começar."
            )
            return render_template("home.html", mensagem=mensagem)
    else:
        servidor = Servidor.query.filter(Servidor.pessoa_id.like(usuario)).first()

        processos = (
            db.session.query(Processo, Atualizacao, Status)
            .select_from(Atualizacao)
            .join(Status)
            .join(Processo)
            .order_by(Atualizacao.id.desc())
            .filter(Processo.servidor_id == servidor.id)
            .group_by(Processo.id)
            .first()
        )

    return render_template("home.html", processos=processos)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/esqueci_minha_senha", methods=["GET", "POST"])
def esqueciSenha():
    if request.method == "GET":
        return render_template("esqueci_minha_senha.html")

    if request.method == "POST":
        email = request.form["inputEmail"]
        token = str(uuid.uuid4())
        existe_email = Pessoa.query.filter_by(email=email).first()
        print(existe_email.token, file=sys.stderr)

        if not existe_email:
            mensagem = "Email não corresponde"
            return render_template("esqueci_minha_senha.html", mensagem=mensagem)

        else:
            existe_email.token = token
            db.session.commit()
            mensagem = "Email de redefinição enviado"
            return render_template("esqueci_minha_senha.html", mensagem=mensagem)


@app.route("/redefinir/<token>", methods=["GET", "POST"])
def redefinirSenha(token):
    if request.method == "GET":
        return render_template("redefinir_senha.html")

    if request.method == "POST":
        tokenAux = str(uuid.uuid4())
        existe_usuario = Pessoa.query.filter_by(token=token).first()

        if existe_usuario:
            if request.form["inputSenha"] == request.form["inputConfirmarSenha"]:
                senha = request.form["inputSenha"]
                senha = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())

                existe_usuario.senha = senha
                existe_usuario.token = tokenAux
                db.session.commit()
            else:
                mensagem = "As senhas não correspondem"
                return render_template("redefinir_senha.html", mensagem=mensagem)

        else:
            mensagem = "Token de redefinição inválido"
            return render_template("erro.html", mensagem=mensagem)

    return render_template("login.html")
