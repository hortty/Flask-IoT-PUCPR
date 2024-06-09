from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from utils.create_db import create_db
from controllers.app_controller import create_app

app = Flask(__name__)

if __name__ == '__main__':
  app = create_app()
  create_db(app)
  app.run(debug=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/logar')
# def logar():
#   return render_template('login.html')

# @app.route('/interface_iot')
# def interface_iot():

#     return render_template('interface_iot.html', param=param)

# @app.route('/cadastro_dados')
# def cadastro_dados():
#   return render_template('cadastro_dados.html')

# @app.route('/sensores')
# def sensores():
#   return render_template('cadastro_sensor.html')

# @app.route('/enviar', methods=['POST'])
# def enviar():
    
#     param = []

#     param.append({'temperatura_maxima': request.form['temperatura_maxima'], 'temperatura_minima': request.form['temperatura_minima'], 'espaco_recipiente': request.form['espaco_recipiente'], 'tipo_medicamento': request.form['tipo_medicamento']})

#     # temperatura_maxima = request.form['temperatura_maxima']
#     # temperatura_minima = request.form['temperatura_minima']
#     # espaco_recipiente = request.form['espaco_recipiente']
#     # tipo_medicamento = request.form['tipo_medicamento']


#     # conn = mysql.connector.connect(**db_config)


#     # cursor = conn.cursor()
#     # cursor.execute("INSERT INTO tabela (temperatura_maxima, temperatura_minima, espaco_recipiente, tipo_medicamento) VALUES (%s, %s, %s, %s)", (temperatura_maxima, temperatura_minima, espaco_recipiente, tipo_medicamento))
#     # conn.commit()


#     # cursor.close()
#     # conn.close()


#     return render_template('interface_iot.html', param=param)

# @app.route('/dados', methods=['POST'])
# def dados():
#     param = []
#     # dados = request.json
#     # temperatura = dados['temperatura']
#     # umidade = dados['umidade']
    
#     return render_template('interface_iot.html', param=param)

# @app.route('/listar_users')
# def listar_users():
#     return render_template('listaruser.html', usuarios=usuarios)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     mensagem = ''

#     if request.method == 'POST':
#         usuario = request.form['usuario']
#         senha = request.form['senha']

#         for user in usuarios:
#             if usuario == user['nome'] and senha == user['senha']:
#                 mensagem = 'Logado com sucesso!'

#             else:
#                 mensagem = 'Usuário ou senha incorretos.'

#     return render_template('login.html', mensagem=mensagem)

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/cadastrar')
# def cadastrar():
#     return render_template('cadastro_user.html')

# @app.route('/cadastro', methods=['GET', 'POST'])
# def cadastro():
#     if request.method == 'POST':

#         nome = request.form['nome']
#         email = request.form['email']
#         senha = request.form['senha']
#         confirmar_senha = request.form['confirmar_senha']
        
#         if not nome or not email or not senha or not confirmar_senha:
#             mensagem = 'Por favor, preencha todos os campos!'
#         elif senha != confirmar_senha:
#             mensagem = 'As senhas não correspondem!'
#         else:
#             usuarios.append({'nome': nome, 'email': email, 'senha': senha})
#             mensagem = 'Cadastro realizado com sucesso!'
    
#     else:
#         mensagem = ''
    
#     return render_template('cadastro_user.html', mensagem=mensagem)

    