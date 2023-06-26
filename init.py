from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LUCASFERNANDES'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from views import views
    import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth.auth, url_prefix='/')
    from models import User, Note

    with app.app_context():
        db.create_all()
        print("database created")
    return app


