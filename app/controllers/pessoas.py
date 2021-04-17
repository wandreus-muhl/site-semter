from app import app, db, login_manager
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from flask_login import login_user, logout_user
from app.models.tables import Pessoa
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
        email = request.form["email"]
        senha = request.form["senha"]

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
    if request.method == "POST":
        nome = request.form["name"]
        email = request.form["email"]
        senha = request.form["password"]
        senhaEcriptada = bcrypt.hashpw(senha.encode("UTF-8"), bcrypt.gensalt())
        contato = request.form["telNumber"]
        data_cadastro = date.today()

        pessoa = Pessoa(
            nome=nome,
            email=email,
            senha=senhaEcriptada,
            contato=contato,
            data_cadastro=data_cadastro,
        )
        db.session.add(pessoa)
        db.session.commit()

    return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@login_manager.unauthorized_handler
def nao_autorizado():
    return redirect(url_for("login", mensagem="Faça login para acessar este recurso"))