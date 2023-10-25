from flask import Blueprint, render_template, redirect, url_for, request, session

views = Blueprint("views", __name__)


@views.route("/")
def root():
    return render_template("login.html")

# START: Define a route for the HTML pages
@views.route("/home")
def home():
    return render_template("home.html")


@views.route("/reviews")
def reviews():
    return render_template("reviews.html")


# Add a new route for the login page
@views.route("/login")
def login_page():
    return render_template("login.html")


# Update the login route to handle form submission and redirect to 'home' on successful login
@views.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Check the credentials against a database or any authentication method you prefer.
    # If the credentials are valid, set up a session to keep the user logged in.

    # Example:
    if username == "example" and password == "password":
        # Here, you can use Flask's built-in session management.
        session["user"] = username

        # Redirect to the "home" route after successful login.
        return redirect(url_for("home"))
    else:
        return "Login failed"

