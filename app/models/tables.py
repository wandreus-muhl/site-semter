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
    token = db.Column(db.String(255))

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
    descricao = db.Column(db.Text)

    def _repr_(self):
        return "<Status tipo %s>" % self.nome


class Atualizacao(db.Model):
    __tablename__ = "atualizacoes"

    id = db.Column(db.Integer, primary_key=True)
    data_atualizacao = db.Column(db.DateTime, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    processo_id = db.Column(db.Integer, db.ForeignKey("processos.id"), nullable=False)


class Terreno(db.Model):
    __tablename__ = "terrenos"

    id = db.Column(db.Integer, primary_key=True)
    lote = db.Column(db.String(10), nullable=False)
    quadra = db.Column(db.String(10), nullable=False)
    setor = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(45), nullable=False)
    bairro = db.Column(db.String(45), nullable=False)
    numero = db.Column(db.Integer, nullable=False)


class Processo(db.Model):
    __tablename__ = "processos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250))
    numero = db.Column(db.String(250))
    tipo_processo = db.Column(db.String(250), nullable=False)
    tipo_lote = db.Column(db.String(250), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_final = db.Column(db.DateTime)
    parecer = db.Column(db.String(250))
    servidor_id = db.Column(db.Integer, db.ForeignKey("servidores.id"))
    contribuinte_id = db.Column(
        db.Integer, db.ForeignKey("contribuintes.id"), nullable=False
    )
    terreno_id = db.Column(db.Integer, db.ForeignKey("terrenos.id"), nullable=False)

    def _repr_(self):
        return "<Processo %d>" % self.cod_processo


class ArquivoProcesso(db.Model):
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
    processo_id = db.Column(db.Integer, db.ForeignKey("processos.id"))


class CheckList(db.Model):
    __tablename__ = "checklist"

    id = db.Column(db.Integer, primary_key=True)
    requerimento = db.Column(db.Boolean)
    CNDPrefeitura = db.Column(db.Boolean)
    CNDSAAE = db.Column(db.Boolean)
    tituloImovel = db.Column(db.Boolean)
    documentacaoEmpresa = db.Column(db.Boolean)
    copiaRG = db.Column(db.Boolean)
    copiaCPF = db.Column(db.Boolean)
    copiaComprovanteResidencia = db.Column(db.Boolean)
    procuracao = db.Column(db.Boolean)
    plantaAssinada = db.Column(db.Boolean)
    elementosCorretos = db.Column(db.Boolean)
    dadosDimensoes = db.Column(db.Boolean)
    proposta = db.Column(db.Boolean)
    locacaoExistentes = db.Column(db.Boolean)
    edificacaoAverbada = db.Column(db.Boolean)
    ARTApresentado = db.Column(db.Boolean)
    memorialDescritivo = db.Column(db.Boolean)
    processo_id = db.Column(db.Integer, db.ForeignKey("processos.id"))
