from flask import render_template, url_for, flash, redirect, request
from lab_bank import app, db, bcrypt
from lab_bank.forms import RegistrationForm, LoginForm, UpdateAccountForm
from lab_bank.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():

    return render_template('home.html', title='Home')  # mágica???


@app.route('/about')
def about():

    return render_template('about.html', title='About')


@app.route('/user/<username>')
def user(username):

    return f'<h1> Usuário: {escape(username)} </h1>'


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Conta criada para {form.username.data}', 'success')

        return redirect(url_for('login')) # or home?

    return render_template('register.html', title='Registrar', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if (user and bcrypt.check_password_hash(user.password, form.password.data)):

            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:

            flash(f'Login incorreto. Verifique email e senha', 'danger')

    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():

    form = UpdateAccountForm()
    profile_picture = url_for('static', filename = 'profile_pictures/' + current_user.profile_picture)

    return render_template('account.html', title='Account', profile_picture = profile_picture, form = form)