from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from lab_bank import db, bcrypt
from lab_bank.models import User, Post
from lab_bank.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from lab_bank.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:

        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Conta criada para {form.username.data}', 'success')

        return redirect(url_for('users.login')) # or home?

    return render_template('register.html', title='Registrar', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:

        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if (user and bcrypt.check_password_hash(user.password, form.password.data)):

            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:

            flash(f'Login incorreto, verifique email e senha', 'danger')

    return render_template('login.html', title='Entrar', form=form)

@users.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('main.home'))
    
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:

            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Sua conta foi atualizada', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_picture = url_for('static', filename = 'profile_pictures/' + current_user.profile_picture)

    return render_template('account.html', title='Account', profile_picture = profile_picture, form = form)
    
@users.route("/user/<string:username>")  
def user_posts(username):

    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 7)
    
    return render_template('user_posts.html', user = user, title = f'Atualizações de {username}', posts = posts)  # mágica???

@users.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    
    if current_user.is_authenticated:
        
        return redirect(url_for('main.home'))
        
    form = RequestResetForm()
    
    if form.validate_on_submit():
        
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        
        flash('Um email foi enviado para alteração da senha', 'info')
        
        return redirect(url_for('users.login'))
    
    return render_template('reset_request.html', title = 'Pedir alteração de senha', form = form)
    
@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    
    if current_user.is_authenticated:
        
        return redirect(url_for('main.home'))
        
    user = User.verify_reset_token(token)
    
    if user is None:
        
        flash('Token inválido ou expirado', 'warning')
        
        return redirect(url_for('users.reset_request'))
        
    form = ResetPasswordForm()
    
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f'Senha alterada com sucesso', 'success')

        return redirect(url_for('users.login')) # or home?
    
    return render_template('reset_password.html', title = 'Alterar a senha', form = form)
    
@users.route("/users")
def user_list():
    users = User.query.all()  # Fetch all users from the database
    return render_template('user_list.html', users=users)