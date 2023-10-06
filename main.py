from website.app import create_app
from flask import render_template

# the reason line 2 works is because website is a python package. So the init.py folder becomes a package. It runs that file and create_app
from website.app import create_app

app = create_app()


# START: Define a route for the html pages
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


# END: Define a route for the html pages

# the below line only allows us to run the server directly via this file
if __name__ == "__main__":
    app.run(
        debug=True
    )  # this runs the flask app and creates a web server. Reruns when changes are made
