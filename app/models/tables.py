from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Pessoa(db.Model, UserMixin):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(45))
    data_cadastro = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Pessoa %s>" % self.nome


class Servidor(db.Model, UserMixin):
    _tablename_ = "servidores"

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10), nullable=False, index=True, unique=True)
    admin = db.Column(db.Boolean, default=0)
    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), nullable=False)

    def _repr_(self):
        return "<Servidor %d>" % self.matricula
