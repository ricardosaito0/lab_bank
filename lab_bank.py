from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from markupsafe import escape
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f5f3e9a5875dabc5b96c185ecec1cd374bdfcf67deecef1c9de698799fe0cabce89e19de1159f3a1a73da9f4070f9e1bcfd77c61c876102a6353d268993a8060fc743350c9efebc1e3e66373a1b4f020'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)
    profile_picture = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60))
    posts = db.relationship('Post', backref = 'author', lazy = True)
    
    def __repr__(self):
        
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"

class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        
        return f"Post('{self.title}', '{self.date_posted}')"

@app.route('/')
@app.route('/home')
def home():

    return render_template('home.html', title = 'Home') #mágica???
    
@app.route('/about')
def about():

    return render_template('about.html', title = 'About')
    
@app.route('/user/<username>')
def user(username):
    return f'<h1> Usuário: {escape(username)} </h1>'
   
@app.route('/register', methods = ['GET', 'POST'])
def register():
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        flash(f'Conta criada para {form.username.data}', 'success')
        
        return redirect(url_for('home'))
    
    return render_template('register.html', title = 'Registrar', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    
    form = LoginForm()
    
    if form.validate_on_submit():
    
        if form.email.data == 'admin@usp.br' and form.password.data == 'psswd':
    
            flash(f'Login feito com sucesso', 'success')
            
            return redirect(url_for('home'))
    
        else:
            
            flash(f'Login incorreto. Verifique email e senha', 'danger')
    
    return render_template('login.html', title = 'Entrar', form = form)
    
if __name__ == '__main__':

    app.run(debug = True)