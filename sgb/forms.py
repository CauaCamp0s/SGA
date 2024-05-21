from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class LivroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor_id = IntegerField('ID do Autor', validators=[DataRequired()])
    ano_publicacao = IntegerField('Ano de Publicação')
    genero = StringField('Gênero')
    disponivel = BooleanField('Disponível')
    submit = SubmitField('Salvar')

class EmprestimoForm(FlaskForm):
    livro_id = SelectField('Livro', coerce=int, validators=[DataRequired()])
    membro_id = SelectField('Membro', coerce=int, validators=[DataRequired()])
    data_emprestimo = DateField('Data de Empréstimo', format='%Y-%m-%d', validators=[DataRequired()])
    data_devolucao = DateField('Data de Devolução', format='%Y-%m-%d')
    submit = SubmitField('Salvar')
