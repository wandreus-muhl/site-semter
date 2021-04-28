from app import app, db, login_manager
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from flask_login import login_user, logout_user
from app.models.tables import Pessoa, Processo
from datetime import date
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
        data_cadastro = date.today()

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

    return redirect("/login")


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
    processos = Processo.query.filter(Processo.contribuinte_id.like(1))

    return render_template("home.html", lista=processos)


@app.route("/pesquisa")
def pesquisa():
    return render_template("pesquisa.html")
