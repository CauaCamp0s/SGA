from flask import render_template, redirect, url_for, request, jsonify
from app import app, db
from models import Autor, Livro, Membro, Emprestimo
from forms import LivroForm, EmprestimoForm

# Restante do código das rotas...


def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

@app.route('/livros')
def livros():
    livros = Livro.query.all()
    return render_template('livros.html', livros=livros)


@app.route('/livros/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    form = LivroForm()
    form.autor_id.choices = [(autor.id, autor.nome) for autor in Autor.query.all()]
    
    if form.validate_on_submit():
        livro = Livro(
            titulo=form.titulo.data,
            autor_id=form.autor_id.data,
            ano_publicacao=form.ano_publicacao.data,
            genero=form.genero.data,
            disponivel=form.disponivel.data
        )
        db.session.add(livro)
        db.session.commit()
        return redirect(url_for('livros'))
    
    return render_template('adicionar_livro.html', form=form)


@app.route('/livros/<int:livro_id>')
def livro_detalhes(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    return render_template('livro_detalhes.html', livro=livro)

@app.route('/livros/<int:livro_id>/editar', methods=['GET', 'POST'])
def editar_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    form = LivroForm(obj=livro)
    if form.validate_on_submit():
        livro.titulo = form.titulo.data
        livro.autor_id = form.autor_id.data
        livro.ano_publicacao = form.ano_publicacao.data
        livro.genero = form.genero.data
        livro.disponivel = form.disponivel.data
        db.session.commit()
        return redirect(url_for('livro_detalhes', livro_id=livro.id))
    return render_template('editar_livro.html', form=form)


@app.route('/livros/<int:livro_id>/excluir', methods=['POST'])
def excluir_livro(livro_id):
    livro = Livro.query.get_or_404(livro_id)
    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for('livros'))



@app.route('/autores', methods=['GET'])
def listar_autores():
    autores = Autor.query.all()
    return render_template('autores.html', autores=autores)

# Rota para adicionar um novo autor via interface web
@app.route('/adicionar_autor', methods=['GET', 'POST'])
def adicionar_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_autor = Autor(nome=nome)
        db.session.add(novo_autor)
        db.session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('adicionar_autor.html')

# Rota para editar um autor via interface web
@app.route('/editar_autor/<int:autor_id>', methods=['GET', 'POST'])
def editar_autor(autor_id):
    autor = Autor.query.get_or_404(autor_id)
    if request.method == 'POST':
        autor.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('editar_autor.html', autor=autor)

# Rota para excluir um autor via interface web
@app.route('/excluir_autor/<int:autor_id>', methods=['POST'])
def excluir_autor_web(autor_id):
    autor = Autor.query.get_or_404(autor_id)
    db.session.delete(autor)
    db.session.commit()
    return redirect(url_for('listar_autores'))

# Rota para criar um novo autor via API
@app.route('/api/autores', methods=['POST'])
def criar_autor():
    data = request.json
    novo_autor = Autor(**data)
    db.session.add(novo_autor)
    db.session.commit()
    return jsonify({'message': 'Autor criado com sucesso!', 'id': novo_autor.id}), 201

# Rota para listar todos os autores via API
@app.route('/api/autores', methods=['GET'])
def listar_autores_api():
    autores = Autor.query.all()
    return jsonify([autor.serialize() for autor in autores]), 200

# Rota para obter detalhes de um autor específico via API
@app.route('/api/autores/<int:id>', methods=['GET'])
def detalhes_autor(id):
    autor = Autor.query.get_or_404(id)
    return jsonify(autor.serialize()), 200

# Rota para atualizar informações de um autor via API
@app.route('/api/autores/<int:id>', methods=['PUT'])
def atualizar_autor(id):
    autor = Autor.query.get_or_404(id)
    data = request.json
    autor.nome = data.get('nome', autor.nome)
    db.session.commit()
    return jsonify({'message': 'Autor atualizado com sucesso!'}), 200

# Rota para excluir um autor via API
@app.route('/api/autores/<int:id>', methods=['DELETE'])
def excluir_autor_api(id):
    autor = Autor.query.get_or_404(id)
    db.session.delete(autor)
    db.session.commit()
    return jsonify({'message': 'Autor excluído com sucesso!'}), 200

@app.route('/emprestimos')
def emprestimos():
    emprestimos = Emprestimo.query.all()
    return render_template('emprestimos.html', emprestimos=emprestimos)
@app.route('/emprestimos/adicionar', methods=['GET', 'POST'])
def adicionar_emprestimo():
    form = EmprestimoForm()
    
    # Obter livros disponíveis
    livros_disponiveis = Livro.query.filter_by(disponivel=True).all()
    form.livro_id.choices = [(livro.id, livro.titulo) for livro in livros_disponiveis]
    
    # Obter todos os membros
    membros = Membro.query.all()
    form.membro_id.choices = [(membro.id, membro.nome) for membro in membros]
    
    if form.validate_on_submit():
        emprestimo = Emprestimo(
            livro_id=form.livro_id.data,
            membro_id=form.membro_id.data,
            data_emprestimo=form.data_emprestimo.data,
            data_devolucao=form.data_devolucao.data
        )
        livro = Livro.query.get(form.livro_id.data)
        livro.disponivel = False  # Marcar o livro como indisponível
        db.session.add(emprestimo)
        db.session.commit()
        return redirect(url_for('emprestimos'))
    
    return render_template('adicionar_emprestimo.html', form=form)


# Rota para criar um novo empréstimo
@app.route('/emprestimos', methods=['POST'])
def criar_emprestimo():
    data = request.json
    novo_emprestimo = Emprestimo(**data)
    db.session.add(novo_emprestimo)
    db.session.commit()
    return jsonify({'message': 'Empréstimo criado com sucesso!', 'id': novo_emprestimo.id}), 201

# Rota para listar todos os empréstimos
@app.route('/emprestimos', methods=['GET'])
def listar_emprestimos():
    emprestimos = Emprestimo.query.all()
    return jsonify([emprestimo.serialize() for emprestimo in emprestimos]), 200

# Rota para obter detalhes de um empréstimo específico
@app.route('/emprestimos/<int:id>', methods=['GET'])
def detalhes_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    return jsonify(emprestimo.serialize()), 200

# Rota para atualizar informações de um empréstimo
@app.route('/emprestimos/<int:id>', methods=['PUT'])
def atualizar_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    data = request.json
    emprestimo.data_devolucao = data.get('data_devolucao', emprestimo.data_devolucao)
    db.session.commit()
    return jsonify({'message': 'Empréstimo atualizado com sucesso!'}), 200

# Rota para excluir um empréstimo
@app.route('/emprestimos/<int:id>', methods=['DELETE'])
def excluir_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({'message': 'Empréstimo excluído com sucesso!'}), 200


@app.route('/membros', methods=['GET'])
def listar_membros():
    membros = Membro.query.all()
    return render_template('membros.html', membros=membros)


@app.route('/adicionar_membro', methods=['GET', 'POST'])
def adicionar_membro_form():
    if request.method == 'POST':
        nome = request.form['nome']
        novo_membro = Membro(nome=nome)
        db.session.add(novo_membro)
        db.session.commit()
        return redirect(url_for('listar_membros'))
    return render_template('adicionar_membro.html')

# Rota para listar todos os membros via API
@app.route('/api/membros', methods=['GET'])
def listar_membros_api():
    membros = Membro.query.all()
    return jsonify([membro.serialize() for membro in membros]), 200

# Rota para criar um novo membro via API
@app.route('/api/membros', methods=['POST'])
def criar_membro_api():
    data = request.json
    novo_membro = Membro(**data)
    db.session.add(novo_membro)
    db.session.commit()
    return jsonify({'message': 'Membro criado com sucesso!', 'id': novo_membro.id}), 201

# Rota para obter detalhes de um membro específico via API
@app.route('/api/membros/<int:id>', methods=['GET'])
def detalhes_membro_api(id):
    membro = Membro.query.get_or_404(id)
    return jsonify(membro.serialize()), 200

# Rota para atualizar informações de um membro via API
@app.route('/api/membros/<int:id>', methods=['PUT'])
def atualizar_membro_api(id):
    membro = Membro.query.get_or_404(id)
    data = request.json
    membro.nome = data.get('nome', membro.nome)
    membro.email = data.get('email', membro.email)
    db.session.commit()
    return jsonify({'message': 'Membro atualizado com sucesso!'}), 200

# Rota para excluir um membro via API
@app.route('/api/membros/<int:id>', methods=['DELETE'])
def excluir_membro_api(id):
    membro = Membro.query.get_or_404(id)
    db.session.delete(membro)
    db.session.commit()
    return jsonify({'message': 'Membro excluído com sucesso!'}), 200



init_routes(app)
