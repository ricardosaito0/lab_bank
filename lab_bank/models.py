from datetime import datetime
from lab_bank import db, login_manager
from flask_login import UserMixin
import pytz
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    subjects = db.relationship('Subject', backref='owner', lazy=True)

    def get_reset_token(self, expire_time = 1800):
        
        s = Serializer(current_app.config['SECRET_KEY'], expire_time)
        
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        
        s = Serializer(current_app.config['SECRET_KEY'])
        
        try:
            
            user_id = s.loads(token)['user_id']
        
        except:
            
            return None
            
        return User.query.get(user_id)

    def __repr__(self):
        
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('America/Sao_Paulo')))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
        

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    lineage = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(50), nullable=False)
    ova_or_control = db.Column(db.String(50), nullable=False)
    dead_or_alive = db.Column(db.String(50), nullable=False)
    acepromazine = db.Column(db.String(50), nullable=False)
    anesthesic = db.Column(db.String(50), nullable=False)
    neuromuscular_blocker = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    project = db.Column(db.String(255), nullable=True)
    naso_anal_length = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    excel_file_path = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
