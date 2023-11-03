from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    jsonify,
)
from .models import Recipe,Review,User
from . import db
from flask_login import login_required, current_user
import json
from sqlalchemy import and_, or_
from sqlalchemy.sql import func

views = Blueprint("views", __name__)


# test comment - bri
# @views.route("/")
# @login_required
# def root():
#     return render_template("home.html")


# START: Define a route for the HTML pages
@views.route("/")
@views.route("/home",methods=['GET','POST'])
@login_required
def home():
    recipe_query = db.session.query(Recipe)
    if request.content_type:
        search = request.args.get('search')
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')

        if search:
            search = "%{}%".format(search)
            recipe_query = recipe_query.filter(Recipe.name.like(search))

        if category:
            recipe_query = recipe_query.filter(Recipe.category_id == category)

        if difficulty:
            recipe_query = recipe_query.filter(Recipe.difficulty_id == difficulty)
        
    recipe_query = recipe_query.all()
    # create dictionary ready to store array of recipes
    recipe_json = {"recipes": []}

    # iterate through recipe_query, and assign db values to dictionary values for frontend
    # each column name defined in the models is the column name in SQL
    for recipe in recipe_query:
        favorited = "true" if (current_user in recipe.users_who_favorited) else None
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
            "favorited" : favorited,
            "category": recipe.category.name,
            "difficulty": recipe.difficulty.difficulty
        }          
        # append dicionary to list in recipes dictionary
        recipe_json["recipes"].append(thisdict)

    if request.content_type:
        return jsonify(recipe_json)
    return render_template("home.html", recipes=recipe_json)

@views.route("/recipe/<int:recipe_id>",methods=['GET','POST'])
@login_required
def recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    reviews = recipe.reviews
    # create dictionary ready to store array of recipes
    
    rating_float = Recipe.query.with_entities(func.avg(Review.stars).label('average')).filter(Review.recipe_id==recipe_id).scalar()
    rating = round(rating_float)
    # iterate through recipe_query, and assign db values to dictionary values for frontend
    # each column name defined in the models is the column name in SQL
    favorited = "true" if (current_user in recipe.users_who_favorited) else None
    recipe = {
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
        "favorited" : favorited,
        "category": recipe.category.name,
        "difficulty": recipe.difficulty.difficulty,
        "rating":rating
    }
    review_json = {"reviews": []}
    for review in reviews:
        user = User.query.get(review.user_id)
        thisdict = {
            "user_id":review.user_id,
            "username":user.username,
            "stars":review.stars,
            "review":review.review
        }
        review_json["reviews"].append(thisdict)
        # append dicionary to list in recipes dictionary

    # if request.content_type:
    #     return jsonify(recipe_json)
    return render_template("recipe.html", recipe=recipe, reviews=review_json)

# Oct 25 - Added Route for About Page
@views.route("/about")
@login_required
def about():
    return render_template("about.html")
@views.route("/review",methods=['GET','POST'])
@login_required
def review():
    if request.method == 'POST':

        recipe_id = request.form.get('recipe_id')
        star_value = request.form.get('star_value')
        review = request.form.get('review')
        existing_review = db.session.query(Review).filter(
            and_(
                Review.recipe_id==recipe_id,
                Review.user_id==current_user.id
            )
        ).all()
        print(existing_review)
        
        if not (existing_review):
            new_review = Review(recipe_id=recipe_id, user_id=current_user.id, stars=star_value, review=review)
            db.session.add(new_review)
            db.session.commit()

    return redirect(url_for('views.recipe',recipe_id=recipe_id))

@views.route('/delete-review', methods=["POST"])
def delete_review():
    json_data = json.loads(request.data)
    recipe_id = json_data['recipe_id']
    
    review = Review.query.get((recipe_id,current_user.id))
    if review:
        db.session.delete(review)
        db.session.commit()
    return jsonify({})
# route for favorites - ANDRES CHECK THIS CODE PLEASE
@views.route("/favorites")
@login_required
def favorites():
    # Query for all recipes (you can use the same code as in the "home" route)
    recipe_query = db.session.query(Recipe).all()

    # Create a dictionary to store the array of recipes
    recipe_json = {"recipes": []}

    # Iterate through recipe_query and assign database values to dictionary values
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
        recipe_json["recipes"].append(thisdict)

    return render_template("favorites.html", recipes=recipe_json)


# route for create
@views.route("/create", methods=['GET','POST'])
@login_required
def create():
    print(current_user.id)
    if request.method == 'POST':
        # get form data
        name = request.form.get('name')
        instructions = request.form.get('instructions')
        hours_to_make = request.form.get('hours_to_make')
        minutes_to_make = request.form.get('minutes_to_make')
        calories = request.form.get('calories')
        description = request.form.get('description')
        image = request.form.get('image')
        ingredients = request.form.get('ingredients')
        category_id = request.form.get('category_id')
        
        # split the lists of instructions and ingredients by the delimiter (temporary solution until tag input is set up)
        instruction_list = instructions.split('|')
        ingredient_list = ingredients.split('|')

        instructions_string = ""
        ingredient_string = ""

        # populate our strings with the array data, separated by delimeters (temporary solution until tag input is set up)
        for i,instruction in enumerate(instruction_list):
            instructions_string = instructions_string + instruction
            if (i < len(instruction_list)-1):
                instructions_string = instructions_string + '|'

        for i,ingredient in enumerate(ingredient_list):
            ingredient_string = ingredient_string + ingredient
            if (i < len(ingredient_list)-1):
                ingredient_string = ingredient_string + '|'
        
        
        new_recipe = Recipe(user_id = current_user.id,name=name,instructions=instructions,hours_to_make=hours_to_make,minutes_to_make=minutes_to_make,calories=calories,description=description,image=image,ingredients=ingredients,category_id=category_id)
        db.session.add(new_recipe)
        db.session.commit()
    return render_template("create.html")


# route for profile (profile icon is the button for it)
@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user = current_user)

# route for profile (profile icon is the button for it)
@views.route("/favoriteToggle", methods=['GET','POST'])
@login_required
def favoriteToggle():
    
    recipe_id = json.loads(request.data)["recipe_id"]
    
    recipe = Recipe.query.get(recipe_id)
    favorited = 1
    if (recipe in current_user.favorites):
        favorited = 0
        current_user.favorites.pop(current_user.favorites.index(recipe))
    else:
        current_user.favorites.append(recipe)
        db.session.add(recipe)    
    db.session.commit()
    return jsonify({"favorited":favorited})

