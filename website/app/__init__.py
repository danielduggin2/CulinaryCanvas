from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app():
    # Specify the correct relative path to the templates  and static folder (lets us use html, css, js)
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # load dotenv dictionary, will look for .env file
    load_dotenv()
    # Set Secret Key to SECRET_KEY from .env
    SECRET_KEY = os.getenv("SECRET_KEY")
    print(SECRET_KEY)
    app.config["SECRET_KEY"] = SECRET_KEY

    # Set DB Name to DB_NAME from .env
    DB_NAME = os.getenv("DB_NAME")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # This tells Flask of new views or URLs
    from .views import views
    from .auth import auth

    # The prefix just helps with navigating files easier. If we did /auth we would have to go get it again.
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Set up Login Manager Default view, initialize
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # import User Model, then use login-manager to load user from session
    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Create tables, "from .models import User" is necessary for this
    with app.app_context():
        db.create_all()

    return app
