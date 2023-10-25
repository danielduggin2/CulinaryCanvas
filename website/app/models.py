from . import db
from flask_login import UserMixin
# from sqlalchemy.sql import func

#ASSOCIATION TABLE
rel_favorites_User_Recipe = db.Table(
    'rel_favorites_User_Recipe',
    db.metadata,
    db.Column('user_id', db.ForeignKey('user.id'), primary_key = True),
    db.Column('recipe_id', db.ForeignKey('recipe.id'), primary_key = True)
)



class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    instructions = db.Column(db.String(1000)) #instructions will be delimited by \~
    hours_to_make = db.Column(db.Integer)
    minutes_to_make = db.Column(db.Integer) #Time Formatting? HH:MM
    calories = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(200))
    ingredients = db.Column(db.String(1000)) #ingredients will be delimited by \~
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #ASSOCIATIONS
    reviews = db.relationship('Review', backref='recipe', lazy=True)
    #BACKREF ASSOCIATIONS
    #category = Category object
    #user = User object
    #users_who_favorited = User Objects
    

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    #ASSOCIATIONS
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    favorites = db.relationship('Recipe', secondary = rel_favorites_User_Recipe, backref='users_who_favorited')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = password=db.Column(db.String(30))
    #ASSOCIATIONS
    recipes = db.relationship('Recipes', backref='category', lazy=True)


class Review(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stars = db.Column(db.Integer)
    review = db.Column(db.String(120))
    #BACKREF ASSOCIATIONS
    #recipe = Recipe Object