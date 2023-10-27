from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from .models import Recipe 
from . import db
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def root():
    return render_template("login.html")

# START: Define a route for the HTML pages
@views.route("/home")
@login_required
def home():
    #query for all recipes
    recipe_query=db.session.query(Recipe).all()
    #create dictionary ready to store array of recipes
    recipe_json = {"recipes":[]}

    #iterate through recipe_query, and assign db values to dictionary values for frontend
    for recipe in recipe_query:
        thisdict = {
            "id": recipe.id,
            "user_id": recipe.user_id,
            "name": recipe.name,
            "instructions": recipe.instructions,
            "hours": recipe.hours_to_make,
            "minutes": recipe.minutes_to_make,
            "calories": recipe.calories,
            "description": recipe.description,
            "image": recipe.image,
            "ingredients": recipe.ingredients,
            "category_id": recipe.category_id,
        }
        #append dicionary to list in recipes dictionary
        recipe_json["recipes"].append(thisdict)
    
    print(recipe_json)
    return render_template("home.html",recipes=recipe_json)


# Oct 25 - Added Route for About Page
@views.route("/about")
@login_required
def about():
    return render_template("about.html")


@views.route("/reviews")
@login_required
def reviews():
    return render_template("reviews.html")


# Add a new route for the login page
# @views.route("/login")
# @login_required
# def login_page():
#     return render_template("login.html")


# # Update the login route to handle form submission and redirect to 'home' on successful login
# @views.route("/login", methods=["POST"])
# @login_required
# def login():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     # Check the credentials against a database or any authentication method you prefer.
#     # If the credentials are valid, set up a session to keep the user logged in.

#     # Example:
#     #Ethan comment here: is below where I need to add the script that runs the queries to pull the usernames and passwords stored in db?
#     if username == "example" and password == "password":
#         # Here, you can use Flask's built-in session management.
#         session["user"] = username

#         # Redirect to the "home" route after successful login.
#         return redirect(url_for("views.home"))
#     else:
#         return "Login failed"
# #signup page-- working bri
# @views.route("/signup")
# @login_required
# def signup_page():
#     return render_template("signup.html")
