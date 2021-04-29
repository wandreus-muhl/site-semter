from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required
from flask_login import login_user, logout_user
from app.models.tables import Pessoa, Processo, Contribuinte
from datetime import date
import bcrypt


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
        data_inicio = date.today()
        contribuinte_id = request.form["getUserID"]

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
