from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'f5f3e9a5875dabc5b96c185ecec1cd374bdfcf67deecef1c9de698799fe0cabce89e19de1159f3a1a73da9f4070f9e1bcfd77c61c876102a6353d268993a8060fc743350c9efebc1e3e66373a1b4f020'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from lab_bank import routes