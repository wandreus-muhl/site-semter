from app import db

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    contato = db.Column(db.String(45))
    data_cadastro = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Pessoa %s>' % self.nome

class Servidor(db.Model):
    __tablename__ = 'servidores'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(10), nullable=False, index=True, unique=True)
    admin = db.Column(db.Boolean, default=0)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)

    def __repr__(self):
        return '<Servidor %s>' % self.matricula