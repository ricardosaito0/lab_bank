from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    
    username = StringField('Insira um nome de usuário', validators = [DataRequired(), Length(min = 1, max = 20)])
    email = StringField('Insira um email', validators = [DataRequired(), Email()])
    password = PasswordField('Defina uma senha', validators = [DataRequired()])
    confirm_password = PasswordField('Repita a senha', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')
    
class LoginForm(FlaskForm):
    
    email = StringField('Insira o email', validators = [DataRequired(), Email()])
    password = PasswordField('Insira a senha', validators = [DataRequired()])
    remember = BooleanField('Lembrar')
    submit = SubmitField('Entrar')