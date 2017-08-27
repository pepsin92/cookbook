from flask import request, render_template, g, Response
from index import app
import sqlite3


def connect_db():
    return sqlite3.connect('recipes.db')


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


def get_tags(rid):
    cur = g.db.cursor()
    cur.execute('SELECT name FROM tag WHERE parent = ?', [rid])
    return [x[0] for x in cur.fetchall()]


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


# @app.route('/<path:path>', methods=['GET'])
# def any_root_path(path):
#     return render_template('index.html')
#
#
# @app.route("/api/user", methods=["GET"])
# @requires_auth
# def get_user():
#     return jsonify(result=g.current_user)
#
#
# @app.route("/api/recipe", methods=["GET"])
# def get_recipe():
#     incoming = request.get_json()
#     id = incoming["id"]
#     recipe = Recipe(id=incoming.id)
#
#
# @app.route("/api/create_user", methods=["POST"])
# def create_user():
#     incoming = request.get_json()
#     user = User(
#         email=incoming["email"],
#         password=incoming["password"]
#     )
#     db.session.add(user)
#
#     try:
#         db.session.commit()
#     except IntegrityError:
#         return jsonify(message="User with that email already exists"), 409
#
#     new_user = User.query.filter_by(email=incoming["email"]).first()
#
#     return jsonify(
#         id=user.id,
#         token=generate_token(new_user)
#     )
#
#
# @app.route("/api/get_token", methods=["POST"])
# def get_token():
#     incoming = request.get_json()
#     user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
#     if user:
#         return jsonify(token=generate_token(user))
#
#     return jsonify(error=True), 403
#
#
# @app.route("/api/is_token_valid", methods=["POST"])
# def is_token_valid():
#     incoming = request.get_json()
#     is_valid = verify_token(incoming["token"])
#
#     if is_valid:
#         return jsonify(token_is_valid=True)
#     else:
#         return jsonify(token_is_valid=False), 403
