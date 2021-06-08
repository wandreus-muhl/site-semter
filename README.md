<h1 align="center">Site SEMTER</h1>

<p align="center">Site desenvolvido para faciltar o trâmite de processos na Secretaria Municipal de Terras de Vilhena-RO. O projeto ocorreu durante a disciplina de Projeto Integrador e de Extensão II - 5 semestre de Análise e Desenvolvimento de Sistemas</p>

<p align="center">
 <a href="#objetivo">Objetivo</a> •
 <a href="#tecnologias">Tecnologias</a> • 
 <a href="#licenca">Licença</a> • 
 <a href="#autor">Autor</a>
</p>

<h4 align="center"> 
	🚧  Em desenvolvimento...  🚧
</h4>

###Pré-requisitos
Para começar, é necessário que tenha instalado em sua máquina as ferramentas:
[Git](https://git-scm.com/) e [Python](https://www.python.org/).

###Rodando o servidor
#Clonando o repositório
$git clone https://github.com/wandreus-muhl/site-semter.git

#Instalando o pipenv
$pip install pipenv

#Acesse a pasta do repositório

#Instalando dependências
$pipenv install

#Executando a aplicação
#Primeiramente, inicie o terminal do pipenv, executando
$pipenv shell

#Depois, execute o arquivo run.py
$python ./run.py

#O servidor será iniciado na porta 5000 - <localhost:5000>

# site-semter

sudo mysql -u root -p 
create database semter; 
create user 'flow'@'localhost' identified by 'flow'; 
grant all privileges on semter.* to 'flow'@'localhost';
