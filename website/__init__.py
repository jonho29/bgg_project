from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'

    from .views import views
    from .saved import saved

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(saved, url_prefix = '/')

    return app