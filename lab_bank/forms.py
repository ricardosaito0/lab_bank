from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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


class UpdateAccountForm(FlaskForm):

    username = StringField('Insira um nome de usuário', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Insira um email', validators=[DataRequired(), Email()])
    picture = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validate_username(self, username):

        if username.data != current_user.username:

            user = User.query.filter_by(username=username.data).first()

            if (user):
                raise ValidationError('Usuário já existente')

    def validate_email(self, email):

        if email.data != current_user.email:

            email = User.query.filter_by(email=email.data).first()

            if (email):
                raise ValidationError('Email já cadastrado')
                
class PostForm(FlaskForm):
    
    title = StringField('Título', validators = [])
    content = TextAreaField('Conteúdo', validators = [])
    submit = SubmitField('Postar')
    
class RequestResetForm(FlaskForm):
    
    email = StringField('Insira o email', validators = [DataRequired(), Email()])
    submit = SubmitField('Pedir alteração de senha')
    
    def validate_email(self, email):

        email = User.query.filter_by(email = email.data).first()

        if email is None:

            raise ValidationError('Não existem contas com esse email')
        
        
class ResetPasswordForm(FlaskForm):
    
    password = PasswordField('Defina uma senha', validators = [DataRequired()])
    confirm_password = PasswordField('Repita a senha', validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Alterar a senha')