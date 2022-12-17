from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

DB_NAME = 'users_database.db'
db = SQLAlchemy()
bcrypt = Bcrypt()
basedir = path.dirname(path.abspath(__file__))


def create_app():  # init script
    app = Flask(__name__)

    # Configs for app
    app.config['SECRET_KEY'] = '76XXq4DegnHFzvr7R6vH6qU54'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    from views import views
    from auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import Users
    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print('DEBUG | Created database')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
