from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from app.models.tables import Pessoa, Processo, Contribuinte, Servidor
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
    contribuinte = Contribuinte.query.filter(Contribuinte.pessoa_id.like(usuario)).first()

    if contribuinte:
        
        id_contribuinte = contribuinte.id
        app.logger.info(
            "O seguinte usuário tentou mostrar seus processos: " + str(id_contribuinte)
        )

        processos = Processo.query.filter(Processo.contribuinte_id.like(id_contribuinte)).all()

        if processos:
            return render_template("home.html", processos=processos)
        else:
            mensagem = "Não há processos criados por este usuário"
            return render_template("home.html", mensagem=mensagem)
    else: 
        processos = Processo.query.all()

    return render_template("home.html", processos=processos)


@app.route("/")
def pesquisa():
    # nome = request.args.get("getUserID")

    # if usuario:
    #     contribuinte = Contribuinte.query.filter(Contribuinte.pessoa_id.like(usuario)).first()
    #     id_contribuinte = contribuinte.id
    #     app.logger.info('O seguinte usuário tentou mostrar seus processos: '+ str(id_contribuinte))

    #     processos = Processo.query.filter(Processo.contribuinte_id.like(id_contribuinte)).all()
    # else:
    #     processos = Processo.query.all()
    return render_template("pesquisa.html")
