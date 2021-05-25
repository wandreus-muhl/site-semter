from app import db
from app.models.tables import Pessoa, Contribuinte, Processo, Status, Servidor
from datetime import datetime, date
import bcrypt

# Criando Status
s1 = Status(nome="Encaminhado", descricao="Encaminhado ao setor da SEMAD") #LARANJA
db.session.add(s1)
db.session.commit()

s2 = Status(nome="Em análise", descricao="O seu processo foi encaminhado para análise") #AMARELO
db.session.add(s2)
db.session.commit()

s3 = Status(nome="Aprovado", descricao="O seu processo foi aprovado!") #VERDE
db.session.add(s3)
db.session.commit()

s4 = Status(nome="Não aprovado", descricao="O seu processo não foi aprovado.") #VERMELHO
db.session.add(s4)
db.session.commit()

s5 = Status(nome="Devolvido", descricao="Existem dependências a serem resolvidas.") #LARANJA
db.session.add(s5)
db.session.commit()