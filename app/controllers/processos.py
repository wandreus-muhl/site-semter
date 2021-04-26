from app import app, db, login_manager
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from flask_login import login_user, logout_user
from app.models.tables import Pessoa
from datetime import date
import bcrypt

@app.route('/processos')
@app.route('/processos/cadastrar')
def cadastrar_processos():
    return render_template("cadastro_processo.html")