from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required
from flask_login import login_user, logout_user
from app.models.tables import Pessoa, Processo, Contribuinte
from datetime import datetime
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
        data_inicio = datetime.now()
       
        contribuinte_id = request.form["getUserID"]
        # Contribuinte.query.filter_by(pessoa_id=contribuinte_id).first()
        contribuinte = Contribuinte.query.filter(Contribuinte.pessoa_id.like(contribuinte_id)).first()

        app.logger.info('O seguinte usuário tentou criar um processo '+contribuinte_id)

        processo = Processo(
            nome=nome,
            numero=numero,
            tipo_processo=tipo_processo,
            tipo_lote=tipo_lote,
            data_inicio=data_inicio,
            contribuinte_id=contribuinte.id
        )
        db.session.add(processo)
        db.session.commit()

    return redirect("/home")
