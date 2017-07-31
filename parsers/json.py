import json
import sqlite3
import re
from sys import stderr
from code import InteractiveConsole
from glob import glob

conn = sqlite3.connect('../recipes.db')


def insert_ingredients(cur, rid, ingreds):
    for i in ingreds:
        if "weight" in i:
            cur.execute('INSERT INTO ingredient (parent, name, weight) VALUES (?, ?, ?)', [rid, i['name'], i['weight']])
        elif "volume" in i:
            cur.execute('INSERT INTO ingredient (parent, name, volume) VALUES (?, ?, ?)', [rid, i['name'], i['volume']])
        else:
            cur.execute('INSERT INTO ingredient (parent, name) VALUES (?, ?)', [rid, i['name']])


def insert_part_ingredients(cur, pid, ingreds)
    for i in ingreds:
        if "weight" in i:
            cur.execute('INSERT INTO ingredient (name, weight) VALUES (?, ?)', [i['name'], i['weight']])
        elif "volume" in i:
            cur.execute('INSERT INTO ingredient (name, volume) VALUES (?, ?)', [i['name'], i['volume']])
        else:
            cur.execute('INSERT INTO ingredient (name) VALUES (?)', [i['name']])
        cur.execute('INSERT INTO recipe_part_ingredient(recipe_part, ingredient) VALUES (?, ?)', [pid, cur.lastrowid])


def tag_recipe(id, tag, cur):
    tag = tag.lower()
    print(tag)
    cur.execute('INSERT INTO tag(parent, name) VALUES (?, ?)', [id, tag])


def insert_part(cur, rid, rp):
    for part in rp:
        cur.execute('INSERT INTO recipe_part(name, body, parent) VALUES (?, ?, ?)', [rp['name'], rp['body'], rid])
        insert_part_ingredients(cur, cur.lastrowid, rp['ingredients'])


def save_json(str):
    with conn:
        cur = conn.cursor()
        recipe = json.loads(str)

        cur.execute('SELECT id FROM recipe WHERE name=?', [recipe["name"]])
        rid = cur.fetchone()
        if rid is None:
            cur.execute('INSERT INTO recipe(name, source) VALUES (?, ?)', [recipe["name"], recipe["source"]])
            rid = cur.lastrowid
            insert_ingredients(cur, rid, recipe["ingredients"])
            for rp in recipe["parts"]:
                insert_part(cur, rid, rp)

        else:
            rid = rid[0]
        for tag in recipe["tags"]:
            tag_recipe(rid, tag, cur)

if __name__ == '__main__':
    test = '''{
        "name":"Cookie",
        "ingredients":[
            {
                "name":"chocolate",
                "weight":"45g"
            }
        ],
        "parts":[
            {
                "name":"Dough",
                "ingredients":[
                    {
                        "name":"sugar",
                        "weight":"1 kg"
                    },
                    {
                        "name":"milk",
                        "volume":"1 fl.oz"
                    }
                ],
                "method":"Mix the ingredients and bake in the solar corona for 0.3 ms."
            }
        ],
        "tags":["sweet", "quick", "stellar"],
        "source":"Imagination"
    }
    '''
    save_json(test)
