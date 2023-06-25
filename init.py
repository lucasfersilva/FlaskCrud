from flask import Flask


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'LUCASFERNANDES'

    from views import views
    import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth.auth, url_prefix='/')

    return app
