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


@app.route("/novo_processo", methods=["GET", "POST"])
def cadastrar_processos():
    if request.method == "GET":
        return render_template("cadastro_processo.html")

    if request.method == "POST":
        nome = request.form["inputName"]
        numero = request.form["inputNumber"]
        tipo_processo = request.form["inputKind"]
        tipo_lote = request.form["inputType"]
        data_inicio = date.today()
        contribuinte_id = current_user.id

        processo = Processo(
            nome=nome,
            numero=numero,
            tipo_processo=tipo_processo,
            tipo_lote=tipo_lote,
            data_inicio=data_inicio,
            contribuinte_id=contribuinte_id,
        )
        db.session.add(processo)
        db.session.commit()

    return redirect("/home")
