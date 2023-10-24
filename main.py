from website.app import create_app
from flask import render_template, redirect, url_for, request, session

app = create_app()


# START: Define a route for the HTML pages
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


# Add a new route for the login page
@app.route("/login")
def login_page():
    return render_template("login.html")


# Update the login route to handle form submission and redirect to 'home' on successful login
@app.route("/login", methods=["POST"])
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


# END: Define a route for the HTML pages

# the below line only allows us to run the server directly via this file
if __name__ == "__main__":
    app.run(
        debug=True
    )  # this runs the Flask app and creates a web server. Reruns when changes are made
