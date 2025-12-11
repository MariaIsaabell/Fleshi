
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from appfleshi.models import User

class PhotoForm(FlaskForm):
    photo = FileField("Foto",validators=[DataRequired()])
    submit = SubmitField("Postar")

class ProfilePhotoForm(FlaskForm):
    photo = FileField("Foto de Perfil", validators=[DataRequired()])
    submit = SubmitField("Salvar Foto")

class LikeForm(FlaskForm):
    submit = SubmitField("Entrar")

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Usuário não encontrado !")
        return None

class RegisterForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome do Usuário", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField("Confirmar senha", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Criar Conta")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E-mail já cadastrado!")
        return None

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Usuário já cadastrado!")
        return None
