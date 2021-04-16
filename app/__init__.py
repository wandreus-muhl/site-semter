from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{{user}}:{{senha}}@localhost/{{db_name}}'
#login_manager = LoginManager(app)
db = SQLAlchemy(app)