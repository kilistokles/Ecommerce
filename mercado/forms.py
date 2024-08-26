from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from mercado.models import User

class CadastroForm(FlaskForm):
    def validate_username(self, check_user):
        user = User.query.filter_by(usuario=check_user.data).first()
        if user:
            raise ValidationError("Usuario ja existe! Cadastre outro nome de usuario")

    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError("E-mail ja existe! Cadastre outro email")

    def validate_senha(self, check_senha):
        senha = User.query.filter_by(senha=check_senha.data).first()
        if senha:
            raise ValidationError("Senha já existe! Escolha outra senha")

    usuario = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail:', validators=[Email(), DataRequired()])
    senha1 = PasswordField(label='Senha:', validators=[Length(min=6), DataRequired()])
    senha2 = PasswordField(label='Confirmação de Senha:', validators=[EqualTo('senha1'), DataRequired()])
    submit = SubmitField(label='Cadastrar')

class LoginForm(FlaskForm):
    usuario = StringField(label="Usuario", validators=[DataRequired()])
    senha = PasswordField(label="Senha", validators=[DataRequired()])
    submit = SubmitField(label="Log In")

class CompraProdutoForm(FlaskForm):
    submit = SubmitField(label="Comprar Produto!")

class VendaProdutoForm(FlaskForm):
    submit = SubmitField(label="Vender Produto!")

class CadastroProd(FlaskForm):
    nome = StringField(label="Nome do produto", validators=[DataRequired()])
    preco = FloatField(label="Preco", validators=[DataRequired()])
    cod_barra = StringField(label="Codigo_barra", validators=[DataRequired()])
    descricao = TextAreaField(label="Descricao", validators=[DataRequired()])
    submit = SubmitField(label="Confirmar")

