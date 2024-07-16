from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lab_bank.models import User

class RegistrationForm(FlaskForm):
    
    username = StringField('Insira um nome de usuário', validators = [DataRequired(), Length(min = 1, max = 20)])
    email = StringField('Insira um email', validators = [DataRequired(), Email()])
    password = PasswordField('Defina uma senha', validators = [DataRequired()])
    confirm_password = PasswordField('Repita a senha', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first()

        if (user):

            raise ValidationError('Usuário já existente')

    def validate_email(self, email):

        email = User.query.filter_by(email = email.data).first()

        if (email):

            raise ValidationError('Email já cadastrado')
    
class LoginForm(FlaskForm):
    
    email = StringField('Insira o email', validators = [DataRequired(), Email()])
    password = PasswordField('Insira a senha', validators = [DataRequired()])
    remember = BooleanField('Lembrar')
    submit = SubmitField('Entrar')