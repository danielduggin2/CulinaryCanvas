from flask import Flask


def create_app():
    # Specify the correct relative path to the templates  and static folder (lets us use html, css, js)
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config["SECRET_KEY"] = "secret key string"
    # This tells Flask of new views or URLs
    from .views import views
    from .auth import auth

    # The prefix just helps with navigating files easier. If we did /auth we would have to go get it again.
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
