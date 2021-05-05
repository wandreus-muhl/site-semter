from app import app, db, login_manager
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from flask_login import login_user, logout_user
from app.models.tables import Pessoa, Processo, Contribuinte, Status, Servidor
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
       
        contribuinte_id = current_user.get_id()
        # Contribuinte.query.filter_by(pessoa_id=contribuinte_id).first()
        contribuinte = Contribuinte.query.filter(Contribuinte.pessoa_id.like(contribuinte_id)).first()

        app.logger.info('O seguinte usuário tentou criar um processo '+str(contribuinte_id))

        processo = Processo(
            nome=nome,
            numero=numero,
            tipo_processo=tipo_processo,
            tipo_lote=tipo_lote,
            data_inicio=data_inicio,
            contribuinte_id=contribuinte.id,
            servidor_id=1
        )
        db.session.add(processo)
        db.session.commit()

    return redirect("/home")

@app.route("/processo/<id_processo>")
def visualizar_processo(id_processo):
    processo = Processo.query.filter_by(id=id_processo).first()

    return render_template("processo.html", processo=processo)

@app.route("/analise_processo", methods=["GET", "POST"])
@login_required
def analisar_processo():

    usuario = current_user.get_id()

    if usuario:
        servidor = Servidor.query.filter(Servidor.pessoa_id.like(usuario)).first()
        id_servidor = servidor.id
        app.logger.info('O seguinte usuário tentou mostrar seus processos: '+ str(id_servidor))

        processos = Processo.query.filter(Processo.servidor_id.like(id_servidor)).all()
    else: 
        processos = Processo.query.all()

    return render_template("analise_processo.html", processos=processos)