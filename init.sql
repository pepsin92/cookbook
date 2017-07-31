CREATE TABLE recipe(
    id INTEGER PRIMARY KEY,
    name TEXT,
    length DATETIME,
    servings INTEGER,
    source TEXT
);

CREATE TABLE recipe_part(
    id INTEGER PRIMARY KEY,
    name TEXT,
    body TEXT,
    parent INTEGER
);

CREATE TABLE ingredient(
    id INTEGER PRIMARY KEY,
    name TEXT,
    volume INTEGER,
    weight INTEGER,
    note TEXT
);

CREATE TABLE tag(
    id INTEGER PRIMARY KEY,
    name TEXT,
    parent INTEGER,
    FOREIGN KEY (parent) REFERENCES recipe(id)
);

-- CREATE TABLE recipe_tag(
--     id INTEGER PRIMARY KEY,
--     recipe INTEGER,
--     tag INTEGER,
--     FOREIGN KEY (recipe) REFERENCES recipe(id),
--     FOREIGN KEY (tag) REFERENCES tag(id)
-- );

CREATE TABLE recipe_ingredient(
    id INTEGER PRIMARY KEY,
    recipe INTEGER,
    ingredient INTEGER,
    FOREIGN KEY (recipe) REFERENCES recipe(id),
    FOREIGN KEY (ingredient) REFERENCES ingredient(id)
);

CREATE TABLE recipe_part_ingredient(
    id INTEGER PRIMARY KEY,
    recipe_part INTEGER,
    ingredient INTEGER,
    FOREIGN KEY (recipe_part) REFERENCES recipe_part(id),
    FOREIGN KEY (ingredient) REFERENCES ingredient(id)
);
