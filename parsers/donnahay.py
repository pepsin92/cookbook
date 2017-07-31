from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import sqlite3
import datetime
from itertools import count
from time import sleep
import re
from sys import stderr
from code import InteractiveConsole

delay = 0
max_comment_age = 30
conn = sqlite3.connect('../recipes.db')
base_url = 'https://www.donnahay.com.au/'


def tag_recipe(id, tag, cur=None):
    if cur is None:
        with conn:
            tag_recipe(id, tag, conn.cursor())

    tag = tag.lower()
    cur.execute('INSERT INTO tag(parent, name) VALUES (?, ?)', [id, tag])


def parse_category(url, tag):
    u = urljoin(base_url, url)
    print("# Parsing category:", tag, file=stderr)
    site = urlopen(u)
    html = BeautifulSoup(site.read(), 'html.parser')
    for a in html.find('div', class_='tiles').find_all('a', href=True):
        download_recipe(urljoin(base_url, a['href']), tag)


def get_method(method):
    res = method.find_all('li')
    # print('method: ', file=stderr)
    res = [max(x.contents, key=len) for x in res]
    # print(res, file=stderr)

    # vars = globals().copy()
    # vars.update(locals())
    # InteractiveConsole(vars).interact()

    return [sanitize(x) for x in res]


def sanitize(s):
    # print(s, file=stderr)
    # print(repr(s.contents))
    try:
        res = s.replace('½', '0.5').replace('¼', '0.25').replace('\xa0', ' ')
    except TypeError:
        s = str(s).partition('>')[2].partition('<')[0]
        # print(s)
        res = s.replace('½', '0.5').replace('¼', '0.25').replace('\xa0', ' ')
    return res


def get_ingredients(ingredients):
    res = ingredients.find_all('li')
    # print('ingredients', file=stderr)
    # print(res[1])
    return [sanitize(max(x.contents, key=len)) for x in res]


def download_recipe(url, tag=None):
    site = urlopen(urljoin(base_url, url))
    html = BeautifulSoup(site.read(), 'html.parser')
    cur = conn.cursor()

    header = html.find('h1', class_='text-center recipe-title__mobile')
    try:
        recipe = header.next.capitalize()
    except TypeError:
        recipe = header.find('p').next.capitalize()
    print('Getting recipe for:', recipe, file=stderr)

    ingredients = get_ingredients(html.find('div', class_='col-sm-6 ingredients'))
    method = get_method(html.find('div', class_='col-sm-6 method'))
    # print(method)
    with conn:
        cur.execute('SELECT id FROM recipe WHERE name=?', [recipe])
        rec = cur.fetchone()
        if rec is None:
            cur.execute('INSERT INTO recipe(name, source) VALUES (?, ?)', [recipe, urljoin(base_url, url)])
            rec = cur.lastrowid
            # cur.executemany('INSERT INTO ingredient (parent, name) VALUES (?, ?)', [[rec, x] for x in ingredients])
            cur.executemany('INSERT INTO recipe_part(parent, name, body) VALUES (?, ?, ?)',
                            [[rec, str(i+1), x] for (i, x) in enumerate(method)])
            for s in ingredients:
                cur.execute('INSERT INTO ingredient (parent, name) VALUES (?, ?)', [rec, s])
                cur.execute('INSERT INTO recipe_ingredient (recipe, ingredient) VALUES (?, ?)', [rec, cur.lastrowid])
        else:
            rec = rec[0]
        if tag is not None:
            tag_recipe(rec, tag, cur)


if __name__ == '__main__':

    parse_category('/recipes/dinner', 'dinner')
    parse_category('/recipes/breakfast', 'breakfast')
    parse_category('/recipes/lunch', 'lunch')
    parse_category('/recipes/snacks-and-sides', 'snack')
    parse_category('/recipes/desserts-and-baking', 'dessert')
    # download_recipe('https://www.donnahay.com.au/recipes/dinner/chicken-noodle-soup')
    # download_recipe('https://www.donnahay.com.au/recipes/dinner/beef-and-caramelised-onion-sausage-rolls')
