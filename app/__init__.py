from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://"
    + os.getenv("DB_USUARIO")
    + ":"
    + os.getenv("DB_PASSWORD")
    + "@"
    + os.getenv("DB_LOCAL")
    + "/"
    + os.getenv("DB_DATABASE")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET")

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

login_manager = LoginManager(app)
login_manager.init_app(app)

from app.controllers import pessoas


@app.route("/home")
def home():
    return render_template("home.html")
