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


@app.route("/cadastro", methods=["GET", "POST"])
def register():
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