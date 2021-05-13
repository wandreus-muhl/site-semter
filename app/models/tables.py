from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Pessoa(db.Model, UserMixin):
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(45))
    data_cadastro = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Pessoa %s>" % self.nome

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome


class Servidor(db.Model, UserMixin):
    __tablename__ = "servidores"

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10), nullable=False, index=True, unique=True)
    admin = db.Column(db.Boolean, default=0)
    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), nullable=False)

    def _repr_(self):
        return "<Servidor %d>" % self.matricula


class Contribuinte(db.Model):
    __tablename__ = "contribuintes"

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(20), nullable=False, index=True, unique=True)
    cnpj = db.Column(db.String(45))
    pessoa_id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), nullable=False)

    def _repr_(self):
        return "<Contribuinte %d>" % self.cpf


class Status(db.Model):
    __tablename__ = "status"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), nullable=False)

    def _repr_(self):
        return "<Status tipo %s>" % self.nome


class Atualizacao(db.Model):
    __tablename__ = "atualizacoes"

    id = db.Column(db.Integer, primary_key=True)
    data_atualizacao = db.Column(db.DateTime, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))


class Processo(db.Model):
    __tablename__ = "processos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250))
    numero = db.Column(db.Integer, nullable=False)
    tipo_processo = db.Column(db.String(250), nullable=False)
    tipo_lote = db.Column(db.String(250), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_final = db.Column(db.DateTime)
    parecer = db.Column(db.String(250))
    servidor_id = db.Column(db.Integer, db.ForeignKey("servidores.id"))
    contribuinte_id = db.Column(
        db.Integer, db.ForeignKey("contribuintes.id"), nullable=False
    )
    atualizacao_id = db.Column(
        db.Integer, db.ForeignKey("atualizacoes.id")
    )  # Quando tiver o status certo de encaminhado, colocar aqui!

    def _repr_(self):
        return "<Processo %d>" % self.cod_processo


class ArquivosProcesso(db.Model):
    __tablename__ = "arquivos"

    id = db.Column(db.Integer, primary_key=True)
    requerimento = db.Column(db.String(45))
    copiaRG = db.Column(db.String(45), nullable=False)
    copiaCPF = db.Column(db.String(45))
    certidaoNegativaPrefeitura = db.Column(db.String(45))
    certidaoNegativaSAAE = db.Column(db.String(45))
    tituloImovel = db.Column(db.String(45))
    copiaComprovanteResidencia = db.Column(db.String(45))
    projetoArt = db.Column(db.String(45))
    documentacaoEmpresa = db.Column(db.String(45))
    procuracao = db.Column(db.String(45))
    processo_id = db.Column(
        db.Integer, db.ForeignKey("processos.id")
    )