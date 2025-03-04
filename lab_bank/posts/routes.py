from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from lab_bank import db
from lab_bank.models import Post
from lab_bank.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
     
    form = PostForm()
    
    if form.validate_on_submit():
        
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Atualização postada', 'success')
        
        return redirect(url_for('main.home'))
     
    return render_template('create_post.html', title='Nova atualização', form = form, legend = 'Nova atualização')
    
@posts.route('/post/<int:post_id>/')
def post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    return render_template('post.html', title = post.title, post = post)
    
@posts.route('/post/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        
        abort(403)
        
    form = PostForm()
    
    if form.validate_on_submit():
        
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Edição bem sucedida', 'success')
        
        return redirect(url_for('posts.post', post_id = post.id))
        
    elif request.method == 'GET':
        
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', title='Editar atualização', form = form, legend = 'Editar atualização')
    
@posts.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user and not current_user.is_admin:
        
        abort(403)
        
    db.session.delete(post)
    db.session.commit()
    flash('Atualização apagada', 'success')
    
    return redirect(url_for('main.home'))