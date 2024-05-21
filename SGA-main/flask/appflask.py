from flask import Flask, jsonify, request, abort, render_template, flash, redirect, url_for, session
import mysql.connector
import logging
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


# Create the Flask app instance
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config['SECRET_KEY'] = 'Caua120400!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:140610@localhost/associacao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


password_hash = generate_password_hash('Caua120400!')

senha_correta = check_password_hash(password_hash, 'Caua120400!')


# Função utilitária para conectar e desconectar do banco de dados
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        # user="caua",
        user="root",
        password="140610",
        database="associacao"
    )


# Função utilitária para executar consultas SQL
def execute_query(sql, values=None, commit=False):
    try:
        db_connection = connect_to_database()
        cursor = db_connection.cursor(dictionary=True)
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)

        if commit:
            db_connection.commit()
            cursor.close()
            db_connection.close()
            return None
        else:
            result = cursor.fetchall()
            cursor.close()
            db_connection.close()
            return result
    except mysql.connector.Error as error:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db_connection' in locals() and db_connection.is_connected():
            db_connection.rollback()
            db_connection.close()
        raise error

 # Rota principal para renderizar a página inicial
# @app.route('/')
# def index():
#     return render_template('index.html')


# Definição da classe User
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Método opcional para representação mais amigável do objeto
    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, email={self.email})"
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(name=name, email=email, password=hashed_password)
        
        try:  
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário registrado com sucesso! Faça o login agora.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Rota para renderizar a página de associados
@app.route('/associados')
def associados():
    try:
        # Consultar todos os associados no banco de dados
        sql = "SELECT * FROM Associados"
        associados = execute_query(sql)
        return render_template('associados.html', associados=associados)
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500


# Rota para renderizar a página de eventos
@app.route('/eventos')
def eventos():
    try:
        # Consulta SQL para obter todos os eventos e os nomes dos associados
        sql = """
            SELECT eventos.*, associados.nome AS nome_associado
            FROM Eventos eventos
            JOIN Associados associados ON eventos.associado_id = associados.associado_id
        """
        # Execute a consulta SQL
        result = execute_query(sql)

        # Converta o resultado da consulta em uma lista de dicionários para jsonify
        eventos = []
        for row in result:
            evento = {
                'evento_id': row['evento_id'],
                'nome_evento': row['nome_evento'],
                'data_evento': row['data_evento'],
                'descricao': row['descricao'],
                'localizacao': row['localizacao'],
                'associado_id': row['associado_id'],
                'nome_associado': row['nome_associado']
            }
            eventos.append(evento)

        # Retorne os eventos como JSON
        return render_template('eventos.html', eventos=eventos, associados=associados)
        return jsonify(eventos), 200
    except Exception as e:
        # Em caso de erro, retorne uma mensagem de erro
        return jsonify({'error': str(e)}), 500

class Associado(db.Model):
    __tablename__ = 'Associados'
    associado_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    endereco = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    tipo_associado = db.Column(db.String(50))
    data_inicio_associacao = db.Column(db.Date)
    data_fim_associacao = db.Column(db.Date)

class Evento(db.Model):
    __tablename__ = 'Eventos'
    evento_id = db.Column(db.Integer, primary_key=True)
    nome_evento = db.Column(db.String(255), nullable=False)
    data_evento = db.Column(db.Date)
    descricao = db.Column(db.Text)
    localizacao = db.Column(db.String(255))
    associado_id = db.Column(db.Integer, db.ForeignKey('Associados.associado_id'), nullable=False)
    associado = db.relationship('Associado', backref=db.backref('eventos', lazy=True))


@app.route('/lista_eventos', methods=['GET', 'POST'])
def lista_eventos():
    if request.method == 'POST':
        try:
            data = request.get_json()
            required_fields = ['nome_evento', 'data_evento', 'descricao', 'localizacao', 'associado_id']
            for field in required_fields:
                if field not in data:
                    raise KeyError(f"Campo obrigatório ausente: {field}")

            novo_evento = Evento(
                nome_evento=data['nome_evento'],
                data_evento=data['data_evento'],
                descricao=data['descricao'],
                localizacao=data['localizacao'],
                associado_id=data['associado_id']
            )
            db.session.add(novo_evento)
            db.session.commit()

            return jsonify({"message": "Evento inserido com sucesso!"}), 201
        except (KeyError, Exception) as error:
            db.session.rollback()
            return jsonify({"error": str(error)}), 400
    else:
        try:
            eventos = Evento.query.all()
            associados = Associado.query.all()
            return render_template('lista_eventos.html', eventos=eventos, associados=associados)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Rota para obter todos os eventos
@app.route('/api/eventos', methods=['GET'])
def get_all_eventos():
    try:
        # Consulta SQL para obter todos os eventos e os nomes dos associados
        sql = """
            SELECT eventos.*, associados.nome AS nome_associado
            FROM Eventos eventos
            JOIN Associados associados ON eventos.associado_id = associados.associado_id
        """
        # Execute a consulta SQL
        result = execute_query(sql)

        # Converta o resultado da consulta em uma lista de dicionários para jsonify
        eventos = []
        for row in result:
            evento = {
                'evento_id': row['evento_id'],
                'nome_evento': row['nome_evento'],
                'data_evento': row['data_evento'],
                'descricao': row['descricao'],
                'localizacao': row['localizacao'],
                'associado_id': row['associado_id'],
                'nome_associado': row['nome_associado']
            }
            eventos.append(evento)

        # Retorne os eventos como JSON
        return jsonify(eventos), 200
    except Exception as e:
        # Em caso de erro, retorne uma mensagem de erro
        return jsonify({'error': str(e)}), 500
        

# @app.route('/api/eventos', methods=['POST'])
# def inserir_evento():
#     try:
#         data = request.get_json()
#         required_fields = ['nome_evento', 'data_evento', 'descricao', 'localizacao', 'associado_id']
#         for field in required_fields:
#             if field not in data:
#                 raise KeyError(f"Campo obrigatório ausente: {field}")

#         sql = "INSERT INTO Eventos (nome_evento, data_evento, descricao, localizacao, associado_id) VALUES (%s, %s, %s, %s, %s)"
#         values = (data['nome_evento'], data['data_evento'], data['descricao'], data['localizacao'], data['associado_id'])
#         execute_query(sql, values, commit=True)

#         return jsonify({"message": "Evento inserido com sucesso!"}), 201
#     except (KeyError, mysql.connector.Error) as error:
#         return jsonify({"error": str(error)}), 400



@app.route('/pagamentos')
def pagamentos():
    try:
        # Consulta SQL para obter todos os pagamentos com os nomes dos associados
        sql = """
            SELECT pagamentos.*, associados.nome AS nome_associado
            FROM Pagamentos pagamentos
            JOIN Associados associados ON pagamentos.associado_id = associados.associado_id
        """
        # Execute a consulta SQL
        result = execute_query(sql)

        # Converta o resultado da consulta em uma lista de dicionários para passar ao template
        pagamentos = []
        for row in result:
            pagamento = {
                'pagamento_id': row['pagamento_id'],
                'data_pagamento': row['data_pagamento'],
                'valor': row['valor'],
                'tipo_pagamento': row['tipo_pagamento'],
                'nome_associado': row['nome_associado']
            }
            pagamentos.append(pagamento)

        # Renderize a página com a lista de pagamentos
        return render_template('pagamentos.html', pagamentos=pagamentos)
    except Exception as e:
        # Em caso de erro, retorne uma mensagem de erro
        return jsonify({'error': str(e)}), 500


# Rota para renderizar a página de cadastro de pagamento
@app.route('/cadastro_pagamento')
def cadastro_pagamento():
    return render_template('cadastro_pagamento.html')

# Rota para obter todos os associados
@app.route('/api/associados', methods=['GET'])
def get_associados():
    try:
        sql = "SELECT * FROM Associados"
        result = execute_query(sql)
        return jsonify(result), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Rota para obter um associado pelo ID
@app.route('/api/associados/<int:associado_id>', methods=['GET'])
def get_associado(associado_id):
    try:
        sql = "SELECT * FROM Associados WHERE associado_id = %s"
        result = execute_query(sql, (associado_id,))
        if not result:
            abort(404, description="Associado não encontrado.")
        return jsonify(result[0]), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Rota para inserir um novo associado
@app.route('/api/associados', methods=['POST'])
def add_associado():
    try:
        data = request.get_json()

        # Verificar se todos os campos obrigatórios estão presentes e não vazios
        required_fields = ['nome', 'endereco', 'email', 'telefone', 'tipo_associado', 'data_inicio_associacao', 'data_fim_associacao']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo obrigatório ausente ou vazio: {field}")

        # Prossiga com a inserção no banco de dados...
        sql = "INSERT INTO Associados (nome, endereco, email, telefone, tipo_associado, data_inicio_associacao, data_fim_associacao) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (
            data['nome'],
            data['endereco'],
            data['email'],
            data['telefone'],
            data['tipo_associado'],
            data['data_inicio_associacao'],
            data['data_fim_associacao']
        )
        execute_query(sql, values, commit=True)

        return jsonify({"message": "Associado inserido com sucesso!"}), 201
    except ValueError as e:
        # Capturar erros de validação de campos
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Capturar erros gerais
        return jsonify({"error": "Erro interno ao processar a requisição"}), 500
# Rota para atualizar um associado existente
@app.route('/api/associados/<int:associado_id>', methods=['PUT'])
def update_associado(associado_id):
    try:
        data = request.get_json()
        required_fields = ['nome', 'endereco', 'email', 'telefone', 'tipo_associado', 'data_inicio_associacao', 'data_fim_associacao']
        
        for field in required_fields:
            if field not in data:
                raise KeyError(f"Campo obrigatório ausente: {field}")

        sql = "UPDATE Associados SET nome = %s, endereco = %s, email = %s, telefone = %s, tipo_associado = %s, data_inicio_associacao = %s, data_fim_associacao = %s WHERE associado_id = %s"
        values = (
            data['nome'],
            data['endereco'],
            data['email'],
            data['telefone'],
            data['tipo_associado'],
            data['data_inicio_associacao'],
            data['data_fim_associacao'],
            associado_id
        )
        execute_query(sql, values, commit=True)

        return jsonify({"message": "Associado atualizado com sucesso!"}), 200
    except (KeyError, Exception) as error:
        return jsonify({"error": str(error)}), 400


# Rota para excluir um associado
@app.route('/api/associados/<int:associado_id>', methods=['DELETE'])
def delete_associado(associado_id):
    try:
        sql_delete_pagamentos = "DELETE FROM Pagamentos WHERE associado_id = %s"
        execute_query(sql_delete_pagamentos, (associado_id,), commit=True)

        sql_delete_associado = "DELETE FROM Associados WHERE associado_id = %s"
        execute_query(sql_delete_associado, (associado_id,), commit=True)

        return jsonify({"message": "Associado excluído com sucesso!"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Rota para obter pagamentos de um associado pelo ID do associado
@app.route('/api/pagamentos/associado/<int:associado_id>', methods=['GET'])
def get_pagamentos_associado(associado_id):
    try:
        sql = "SELECT * FROM Pagamentos WHERE associado_id = %s"
        result = execute_query(sql, (associado_id,))
        return jsonify(result), 200
    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500

# Rota para adicionar um novo pagamento
@app.route('/api/pagamentos', methods=['POST'])
def add_pagamento():
    try:
        data = request.get_json()

        # Verificar se todos os campos obrigatórios estão presentes
        required_fields = ['associado_id', 'data_pagamento', 'valor', 'tipo_pagamento']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo obrigatório ausente ou vazio: {field}")

        # Extrair os dados do JSON recebido
        associado_id = data['associado_id']
        data_pagamento = data['data_pagamento']
        valor = data['valor']
        tipo_pagamento = data['tipo_pagamento']

        # Inserir o pagamento no banco de dados
        sql = "INSERT INTO Pagamentos (associado_id, data_pagamento, valor, tipo_pagamento) VALUES (%s, %s, %s, %s)"
        values = (associado_id, data_pagamento, valor, tipo_pagamento)
        execute_query(sql, values, commit=True)

        return jsonify({"message": "Pagamento inserido com sucesso!"}), 201

    except (KeyError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 404

# Create the Flask app instance















# ROTAS PARA EDITAR E EXCLUIR ASSOCIADOS, EVENTOS E PAGAMENTOS



# Rota para a página de edição de associado
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_associado(id):
    try:
        if request.method == 'GET':
            # Busca o associado pelo ID
            sql = "SELECT * FROM Associados WHERE associado_id = %s"
            associado = execute_query(sql, (id,))
            if not associado:
                return "Associado não encontrado."
            return render_template('editar_associado.html', associado=associado[0])
        elif request.method == 'POST':
            # Atualiza os detalhes do associado no banco de dados
            nome = request.form['nome']
            email = request.form['email']
            tipo_associado = request.form['tipo_associado']
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']

            sql = "UPDATE Associados SET nome = %s, email = %s, tipo_associado = %s, data_inicio_associacao = %s, data_fim_associacao = %s WHERE associado_id = %s"
            values = (nome, email, tipo_associado, data_inicio, data_fim, id)
            execute_query(sql, values, commit=True)

            return redirect('/associados')  # Redireciona para a lista de associados após a edição
    except Exception as e:
        return str(e)


# Rota para a exclusão de associado
@app.route('/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_associado(id):
    try:
        if request.method == 'GET':
            # Busca o associado pelo ID para exibir os detalhes antes da exclusão
            sql = "SELECT * FROM Associados WHERE associado_id = %s"
            associado = execute_query(sql, (id,))
            if not associado:
                return "Associado não encontrado."

            return render_template('excluir_associado.html', associado=associado[0])
        elif request.method == 'POST':
            # Exclui o associado do banco de dados
            sql = "DELETE FROM Associados WHERE associado_id = %s"
            execute_query(sql, (id,), commit=True)
            
            return redirect('/associados')  # Redireciona para a lista de associados após a exclusão
    except Exception as e:
        return str(e)


@app.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
def editar_evento(id):
    try:
        if request.method == 'GET':
            # Busca o evento pelo ID
            sql = "SELECT * FROM Eventos WHERE evento_id = %s"
            evento = execute_query(sql, (id,))
            if not evento:
                return "Evento não encontrado."
            return render_template('editar_evento.html', evento=evento[0])
        elif request.method == 'POST':
            # Atualiza os detalhes do evento no banco de dados
            nome_evento = request.form['nome_evento']
            data_evento = request.form['data_evento']

            sql = "UPDATE Eventos SET nome_evento = %s, data_evento = %s WHERE evento_id = %s"
            values = (nome_evento, data_evento, id)
            execute_query(sql, values, commit=True)

            return redirect('/eventos')  # Redireciona para a lista de eventos após a edição
    except Exception as e:
        return str(e)



@app.route('/excluir_evento/<int:id>', methods=['GET', 'POST'])
def excluir_evento(id):
    try:
        if request.method == 'GET':
            # Busca o evento pelo ID
            sql = "SELECT * FROM Eventos WHERE evento_id = %s"
            evento = execute_query(sql, (id,))
            if not evento:
                return "Evento não encontrado."
            return render_template('excluir_evento.html', evento=evento[0])
        elif request.method == 'POST':
            # Remove o evento do banco de dados
            sql = "DELETE FROM Eventos WHERE evento_id = %s"
            execute_query(sql, (id,), commit=True)

            return redirect('/eventos')  # Redireciona para a lista de eventos após a exclusão
    except Exception as e:
        return str(e)



@app.route('/editar_pagamento/<int:id>', methods=['GET', 'POST'])
def editar_pagamento(id):
    try:
        if request.method == 'GET':
            # Busca o pagamento pelo ID
            sql = "SELECT * FROM Pagamentos WHERE pagamento_id = %s"
            pagamento = execute_query(sql, (id,))
            if not pagamento:
                return "Pagamento não encontrado."
            return render_template('editar_pagamento.html', pagamento=pagamento[0])
        elif request.method == 'POST':
            # Atualiza os detalhes do pagamento no banco de dados
            data_pagamento = request.form['data_pagamento']
            valor = request.form['valor']
            tipo_pagamento = request.form['tipo_pagamento']

            sql = "UPDATE Pagamentos SET data_pagamento = %s, valor = %s, tipo_pagamento = %s WHERE pagamento_id = %s"
            values = (data_pagamento, valor, tipo_pagamento, id)
            execute_query(sql, values, commit=True)

            return redirect('/pagamentos')  # Redireciona para a lista de pagamentos após a edição
    except Exception as e:
        return str(e)
    
    

@app.route('/excluir_pagamento/<int:id>', methods=['GET', 'POST'])
def excluir_pagamento(id):
    try:
        if request.method == 'GET':
            # Busca o pagamento pelo ID
            sql = "SELECT * FROM Pagamentos WHERE pagamento_id = %s"
            pagamento = execute_query(sql, (id,))
            if not pagamento:
                return "Pagamento não encontrado."
            return render_template('excluir_pagamento.html', pagamento=pagamento[0])
        elif request.method == 'POST':
            # Remove o pagamento do banco de dados
            sql = "DELETE FROM Pagamentos WHERE pagamento_id = %s"
            execute_query(sql, (id,), commit=True)

            return redirect('/pagamentos')  # Redireciona para a lista de pagamentos após a exclusão
    except Exception as e:
        return str(e)

    
    

if __name__ == '__main__':
    with app.app_context():
        db.session.remove()  # Certifique-se de estar dentro do contexto da aplicação Flask
    app.run(debug=True)