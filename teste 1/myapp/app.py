import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from dotenv import load_dotenv
import requests

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
#login_manager = LoginManager(app)
#login_manager.login_view = 'login'
API_KEY = os.getenv('DEEPSEEK_API_KEY')

# --- Modelos ---
#class User(db.Model, UserMixin):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(80), unique=True, nullable=False)
#    password = db.Column(db.String(200), nullable=False)

#@login_manager.user_loader
# def load_user(user_id):
#    return User.query.get(int(user_id))

# --- Rotas ---
@app.route('/')
def index():
    # dados de veículos fictícios (substituir por consulta ao DB)
    carros = [
        {'nome':'Ferrari F8', 'imagem':'f8.jpg'},
        {'nome':'Porsche 911', 'imagem':'porsche.jpg'}
    ]
    return render_template('index.html', carros=carros)

@app.route('/veiculos')
def veiculos():
    carros = [
        {'nome':'Ferrari F8', 'imagem':'f8.jpg'},
        {'nome':'Porsche 911', 'imagem':'porsche.jpg'}
    ]
    return render_template('veiculos.html', carros=carros)

@app.route('/contato', methods=['GET','POST'])
def contato():
    if request.method == 'POST':
        # processa formulário de contato
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        # aqui você pode salvar no DB ou enviar e-mail
        return redirect(url_for('index'))
    return render_template('contato.html')

@app.route('/login', methods=['GET','POST'])
def login():
    #if request.method == 'POST':
    #    user = User.query.filter_by(username=request.form['username']).first()
    #    if user and user.password == request.form['password']:
    #        login_user(user)
    #       return redirect(url_for('index'))
    return render_template('login.html')

#@app.route('/logout')
#@login_required
def logout():
    #logout_user()
    return redirect(url_for('index'))

# --- Endpoint do Chatbot ---
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    prompt = data.get('message', '')

    # 2) Monta o payload de chat e faz o POST
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'deepseek-chat',   # troque depois que souber o nome exato
        'messages': [
            {'role': 'system', 'content': 'Você é um assistente para GWM Motor Sport.'},
            {'role': 'user',   'content': prompt}
        ]
    }

    r = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        json=payload, headers=headers)

    # Em vez de r.raise_for_status(), trate o erro para imprimir o body:
    if r.status_code != 200:
        print("=== DeepSeek ERROR ===")
        print("STATUS:", r.status_code)
        print("REQUEST JSON:", payload)
        print("RESPONSE TEXT:", r.text)
        return jsonify({'error': 'DeepSeek Bad Request', 'detail': r.text}), 500

    return jsonify(r.json())



