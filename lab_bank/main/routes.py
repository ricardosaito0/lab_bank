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
    
    test_table_hiragana = [
        ['', 'あ', 'い ', 'う', 'え', 'お'],
        ['k', 'か', 'き', 'く', 'け', 'こ'],
        ['s', 'さ', 'し', 'す', 'せ', 'そ'],
        ['t', 'た', 'ち', 'つ', 'て', 'と'],
        ['n', 'な', 'に', 'ぬ', 'ね', 'の'],
        ['h', 'は', 'ひ', 'ふ', 'へ', 'ほ'],
        ['m', 'ま', 'み', 'む', 'め', 'も'],
        ['y', 'や', '', 'ゆ', '', 'よ'],
        ['r', 'ら', 'り', 'る', 'れ', 'ろ'],
        ['w', 'わ', '', '', '', 'を'],
        ['n', 'ん', '', '', '', '']
        ]
    df_hiragana = pd.DataFrame(test_table_hiragana, columns = ['', 'a', 'i', 'u', 'e', 'o'])
    test_table_hiragana_html = df_hiragana.to_html(classes='table table-striped', index=False)


    test_table_katakana = [
        ['', 'ア', 'イ', 'ウ', 'エ', 'オ'],
        ['k', 'カ', 'キ', 'ク', 'ケ', 'コ'],
        ['s', 'サ', 'シ', 'ス', 'セ', 'ソ'],
        ['t', 'タ', 'チ', 'ツ', 'テ', 'ト'],
        ['n', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ'],
        ['h', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ'],
        ['m', 'マ', 'ミ', 'ム', 'メ', 'モ'],
        ['y', 'ヤ', '', 'ユ', '', 'ヨ'],
        ['r', 'ラ', 'リ', 'ル', 'レ', 'ロ'],
        ['w', 'ワ', '', '', '', 'ヲ'],
        ['n', 'ン', '', '', '', '']
        ]

    df_katakana = pd.DataFrame(test_table_katakana, columns=['', 'a', 'i', 'u', 'e', 'o'])

    test_table_katakana_html = df_katakana.to_html(classes='table table-striped', index=False)



    return render_template('about.html', title='About', legend = 'Sobre a página', test_table_hiragana = test_table_hiragana_html, test_table_katakana = test_table_katakana_html)