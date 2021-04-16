from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods= ['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods= ['GET', 'POST'])
def register():
    return render_template('register.html')

app.run()