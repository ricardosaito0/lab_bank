from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate  # Import Flask-Migrate
from lab_bank.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with the app and db

    from lab_bank.users.routes import users
    from lab_bank.posts.routes import posts
    from lab_bank.main.routes import main
    from lab_bank.table.routes import table
    from lab_bank.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(table)
    app.register_blueprint(errors)
    
    return app