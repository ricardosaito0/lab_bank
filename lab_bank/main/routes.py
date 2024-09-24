from flask import render_template, request, Blueprint
from lab_bank.models import Post
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():

    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 7)
    return render_template('home.html', title = 'Página Inicial', posts = posts)  # mágica???


@main.route('/about')
def about():
    
    test_table = [[78, 21, 41], [12, 34, 12], [12334, 5646, 213213], [4213, 12312, 234]]
    df = pd.DataFrame(test_table, columns = ['a', 'b', 'c'])
    test_table_html = df.to_html(classes='table table-striped', index=False)

    return render_template('about.html', title='About', test_table = test_table_html)