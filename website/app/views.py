from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/")  # this helps with navigation
def home():
    return "<h1>Hello</h1>"  # returns this as a h1 tag (for testing)
