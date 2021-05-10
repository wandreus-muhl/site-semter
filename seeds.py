from app import db
from app.models.tables import Pessoa, Contribuinte, Processo, Status, Servidor
from datetime import datetime
import bcrypt

# #Criando pessoas
# senha_plana = 'flow' 
# senha_encriptada = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())
# p1 = Pessoa(nome='Nelson Treméa Neto', email='nelson.tremea@gmail.com', senha=senha_encriptada, data_cadastro=datetime.now(), cpf="123.456.789-10")
# db.session.add(p1)
# db.session.commit()

#Criando contribuinte
c1 = Contribuinte(cpf=p1.cpf, pessoa_id=4)
db.session.add(c1)
db.session.commit()

# Criando Status
# s1 = Status(nome="Encaminhado", descricao="Encaminhado ao setor da SEMAD", data_atualizacao=date.today())
# db.session.add(s1)
# db.session.commit()

# p1 = Processo(nome="Minha casa", numero=2620, tipo_processo="Desmembramento", tipo_lote="Lote Urbano", data_inicio=date.today(), contribuinte_id=1)
# db.session.add(p1)
# db.session.commit()

# c1 = Contribuinte(cpf=12345656710, pessoa_id=5)
# db.session.add(c1)
# db.session.commit()

# # Criando status
# s1 = Status(nome="Em análise", descricao="O seu processo foi encaminhado para análise", data_atualizacao=datetime.now())
# db.session.add(s1)
# db.session.commit()

# s1 = Servidor(matricula="12345", admin=True, pessoa_id=p1.id)
# db.session.add(s1)
# db.session.commit()