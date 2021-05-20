from app import db
from app.models.tables import Pessoa, Contribuinte, Processo, Status, Servidor
from datetime import datetime, date
import bcrypt

# Criando contribuinte
senha_plana = "flow"
senha_encriptada = bcrypt.hashpw(senha_plana.encode("utf-8"), bcrypt.gensalt())
p1 = Pessoa(
    nome="Wandreus Mühl Dourado",
    email="wandreusmuhl70@gmail.com",
    senha=senha_encriptada,
    contato="(69) 91111-1111",
    data_cadastro=datetime.now(),
    cpf="123.456.789-10",
)
db.session.add(p1)
db.session.commit()

c1 = Contribuinte(cpf=p1.cpf, pessoa_id=p1.id)
db.session.add(c1)
db.session.commit()

# Criando servidor
senha_plana = "flow"
senha_encriptada = bcrypt.hashpw(senha_plana.encode("utf-8"), bcrypt.gensalt())
p2 = Pessoa(
    nome="Clayton Xavier",
    email="clayton@mail.com",
    senha=senha_encriptada,
    contato="(69) 91211-1111",
    data_cadastro=datetime.now(),
    cpf="123.456.789-11",
)
db.session.add(p1)
db.session.commit()

s1 = Servidor(matricula="12345", admin=True, pessoa_id=p1.id)
db.session.add(s1)
db.session.commit()

# Criando processos
p1 = Processo(
    nome="Minha casa",
    numero=2620,
    tipo_processo="Desmembramento",
    tipo_lote="Lote Urbano",
    data_inicio=date.today(),
    contribuinte_id=c1.id,
)
db.session.add(p1)
db.session.commit()

# Criando Status
s1 = Status(nome="Encaminhado", descricao="Encaminhado ao setor da SEMAD")
db.session.add(s1)
db.session.commit()

s2 = Status(nome="Em análise", descricao="O seu processo foi encaminhado para análise")
db.session.add(s2)
db.session.commit()
