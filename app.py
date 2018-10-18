from flask import request, render_template, g, Response
from index import app
import sqlite3
import re
import os
import errno


def connect_db():
    return sqlite3.connect('recipes.db')

#OLD
def get_recipe_by_id(rid):
    cur = g.db.cursor()
    cur.execute('SELECT name FROM recipe WHERE id=?', [rid])
    name = cur.fetchone()
    if name is None:
        return None
    name = name[0]

    res = {'name': name}
    cur.execute('SELECT name FROM ingredient WHERE id in (SELECT ingredient FROM recipe_ingredient WHERE recipe=?)', [rid])
    res['ingredients'] = [{'name': x[0]} for x in cur.fetchall()]
    cur.execute('SELECT name, body FROM recipe_part WHERE parent=? ORDER BY id', [rid])
    res['parts'] = [{'name': x[0], 'body': x[1]} for x in cur.fetchall()]
    cur.execute('SELECT name FROM tag WHERE parent=?', [rid])
    res['tags'] = [{'name': x[0]} for x in cur.fetchall()]
    return res

#NEW
def get_recipe_by_name(recipe_name):
	path = "standardized_recipes/" + recipe_name
	recipe_file = open(path + "/" + recipe_name + ".xml", "w+")
	print(recipe_file)
	#TODO get recipe from xml
	res = {'name': }
	

#OLD
def get_tags(rid):
    cur = g.db.cursor()
    cur.execute('SELECT name FROM tag WHERE parent = ?', [rid])
    return [x[0] for x in cur.fetchall()]
#NEW
def get_tags(name):
	path = "standardized_recipes/" + recipe_name
	recipe_file = open(path + "/" + recipe_name + ".xml", "w+")
	#TODO get tags from xml


#OLD
def get_recipes(tag = None):
    cur = g.db.cursor()
    if tag is not None:
        cur.execute('SELECT id, name FROM recipe WHERE id IN (SELECT parent FROM tag WHERE name=?) ORDER BY name', [tag])
    else:
        cur.execute('SELECT id, name FROM recipe ORDER BY name')
    res = []
    for recipe in cur.fetchall():
        d = {"id": recipe[0],
             "name": recipe[1],
             "tags": get_tags(recipe[0])
             }
        res.append(d)
    return res

#NEW
def get_recipes(tag = None):
	res = []
	if tag is None:
		res = ls standardized_recipes/
	else:
		#get a list of recipes
		#return those that have matching tag in db
	return res

#OLD
def add_tag(rid, tag):
    cur = g.db.cursor()
    cur.execute('SELECT id FROM tag WHERE parent=?', [rid])
    if cur.fetchone() is None:
        return
    cur.execute('SELECT id FROM tag WHERE parent=? AND name=?', [rid, tag])
    if cur.fetchone() is not None:
        return
    cur.execute('INSERT INTO tag(parent, name) VALUES (?, ?)', [rid, tag])

    g.db.commit()

#NEW
def add_tag(name, tag)
	#Add it into xml file
	#Change it in the database

#TODO Also do removing tags

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', recipes=get_recipes())

@app.route('/tagsearch/', methods=['GET'])
def tagsearch():
    print('hi')
    t = request.form['term']
    return tag(t)


@app.route('/tag/<tag>')
def tag(tag):
    return render_template('index.html', recipes=get_recipes(tag))


@app.route('/recipe/<rid>', methods=['POST', 'GET'])
def recipe(rid):
    rid = int(rid)
    if request.method == 'POST':
        new_tag = request.form['add_tag']
        add_tag(rid, new_tag)
    recipe = get_recipe_by_id(rid)
    return render_template('recipe.html', recipe=recipe)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    #get recipe properties DONE
    recipe_name = request.form['recipeName']
    recipe_time = request.form['recipeTime']
    recipe_serving_num = request.form['servingsNumber']
    recipe_source = request.form['recipeSource']
    #get recipe tags, format them
    recipe_tags = [tag.strip() for tag in request.form['recipeTags'].split(',')]
    #get a list of ingredients
    ingredient_list = []
    ingredient_id = 1
    while ("ingredient" + str(ingredient_id)) in request.form:
        #TODO: Add ingredient note property
        ingredient_list.append([request.form["ingredient" + str(ingredient_id)], request.form["amount" + str(ingredient_id)], request.form["unit" + str(ingredient_id)]])
        ingredient_id += 1
    #print(ingredient_list)
    #I could check whether you added any ingredients here, but screw it, if you
    #want a recipe with no ingredients, then you can have it.

    #get a list of steps
    steps = []
    step_id = 1
    while ("step" + str(step_id)) in request.form:
        steps.append(request.form["step" + str(step_id)])
        step_id += 1
    #print(steps)
    #Ditto with the steps

    #write recipe into a file

    #making a folder
    path = "standardized_recipes/" + str(recipe_name)
    duplicated_recipe_id = 1
    while True:
        try:
            os.makedirs(path)
            break
        except OSError as e:
            if e.errno == errno.EEXIST:
                duplicated_recipe_id += 1
                recipe_name = request.form['recipeName'] + str(duplicated_recipe_id)
                path = "standardized_recipes/" + recipe_name
            else:
                #TODO: return error message to html instead of terminal
                print(e)
                raise
    #creating a recipe file
    file_name = recipe_name + str(duplicated_recipe_id) +".xml"
    #print(path)
    recipe_file = open(path + "/" + recipe_name + ".xml", "w+")
    #writing the recipe into the file
    #TODO: Fix this too
    #Write recipe properties
    recipe_file.write("<title>"+request.form['recipeName']+"</title>\n")
    recipe_file.write("\n")
    recipe_file.write("<time_min>" + recipe_time + "</time_min>\n")
    recipe_file.write("<servings>" + recipe_serving_num + "</servings>\n")
    recipe_file.write("<source>" + recipe_source + "</source>\n")
    #Write recipe tags
    recipe_file.write("<tags>\n")
    #TODO: Add choice from existing tags
    for tag in recipe_tags:
        recipe_file.write("\t<tag>" + tag + "</tag>\n")
    recipe_file.write("</tags>\n\n")

    #Write recipe ingredients
    #TODO: Add possibility of multiple named ingredient lists
    recipe_file.write("<ingredients_list>\n")

    recipe_file.write("<list_title></list_title>\n")
    for ingredient in ingredient_list:
        recipe_file.write("\t<ingredient>\n")
        #TODO: Do this for general number of ingredient properties instead of 0, 1, 2...
        recipe_file.write("\t\t<name>" + ingredient[0] + "</name>\n")
        recipe_file.write("\t\t<amount>" + ingredient[1] + "</amount>\n")
        recipe_file.write("\t\t<unit>" + ingredient[2] + "</unit>\n")
        recipe_file.write("\t\t<note>""</note>\n")

        recipe_file.write("\t</ingredient>\n")
    recipe_file.write("</ingredients_list>\n")
    recipe_file.write("\n")

    #Write directions
    recipe_file.write("<directions>\n")
    for step in steps:
        recipe_file.write("\t<step>" + step + "</step>\n")

    recipe_file.write("</directions>\n")


    #TODO: Do a recipe part (ingredients + directions) insted of multiple ingredient lists?

    print("Adding a new recipe")
    return "Good boye!"
