from flask import render_template, request, Blueprint
from lab_bank.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():

    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 7)
    return render_template('home.html', title = 'Página Inicial', posts = posts)  # mágica???


@main.route('/about')
def about():

    return render_template('about.html', title='About')