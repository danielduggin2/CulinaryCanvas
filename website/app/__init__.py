from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret key string"

    # this tells flask of new views or urls
    from .views import views
    from .auth import auth

    # the prefix just helps with naviating files easier. If we did /auth we would have to go get it again.
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
