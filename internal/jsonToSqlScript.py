import json

#open json file
recipe_json = open("CulinaryCanvas/internal/recipe.json", "r").read()

#open sql file
f = open("CulinaryCanvas/internal/populateRecipes.sql", "w",encoding='utf-8')


script_string = '''INSERT INTO recipe (user_id,name,instructions,hours_to_make,minutes_to_make,calories,description,image,ingredients,category_id)
VALUES 
'''
#iterate through all recipes in json
for i,recipe in enumerate(json.loads(recipe_json)['recipes']):

  #create a string delimited by ¦ from array of instructions
  instructions_string = ""
  for j,instruction in enumerate(recipe["instructions"]):
    instructions_string = instructions_string + instruction
    if j < len(recipe["instructions"])-1:
      instructions_string = instructions_string + "¦"

  #create a string delimited by ¦ from array of ingredients
  ingredients_string = ""
  for j,ingredient in enumerate(recipe["ingredients"]):
    ingredients_string = ingredients_string + ingredient
    if j < len(recipe["ingredients"])-1:
      ingredients_string = ingredients_string + "¦"

  #formatted string to put json values in VALUES part of INSERT statement
  script_string = script_string + '({user_id},"{name}","{instructions}",{hours_to_make},{minutes_to_make},{calories},"{description}","{image}","{ingredients}",{category_id})'.format(
        user_id=1,
        name=recipe["recipe_name"],
        instructions=instructions_string,
        hours_to_make=0,
        minutes_to_make=int(''.join(filter(str.isdigit, recipe["time"]))),
        calories=int(''.join(filter(str.isdigit, recipe["calories"]))),
        description=recipe["description"],
        image=recipe["image"],
        ingredients=ingredients_string,
        category_id=1)
  
  #insert ";" if last recipe, "," else
  if i < len(json.loads(recipe_json)['recipes'])-1:
    script_string = script_string + ",\n"
  else:
    script_string = script_string + ";\n"

#write to file
f.write(script_string)