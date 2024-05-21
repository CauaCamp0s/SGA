from app import db

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    livros = db.relationship('Livro', backref='autor', lazy=True)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    emprestimos = db.relationship('Emprestimo', backref='livro', lazy=True)

class Membro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    emprestimos = db.relationship('Emprestimo', backref='membro', lazy=True)

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    membro_id = db.Column(db.Integer, db.ForeignKey('membro.id'), nullable=False)
    data_emprestimo = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date, nullable=True)
