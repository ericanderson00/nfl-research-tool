
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager
import requests, json

db = SQLAlchemy()
# migrate = Migrate()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'askjhdakjsbd akidkweid'
    app.config['SQLALCHEMY_DATABASE_URI'] =f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # migrate.init_app(app, db, render_as_batch=True)
    
    migrate = Migrate(app, db)
    
    
    

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note, PlayerInfo #make sure that it defines teh db classes in models.py
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    create_database(app)
    return app

def create_database(app):
    with app.app_context():    
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')