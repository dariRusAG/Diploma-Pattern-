import sqlite3
con = sqlite3.connect("DB.sqlite")

con.executescript('''
CREATE TABLE IF NOT EXISTS category (
 category_id INTEGER PRIMARY KEY AUTOINCREMENT,
 category_name VARCHAR(30)
);

INSERT INTO category (category_name)
VALUES
('Брюки'),
('Платья'),
('Рубашки'),
('Футболки'),
('Юбки');


CREATE TABLE IF NOT EXISTS pattern (
 pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
 pattern_name VARCHAR(70),
 category_id INTEGER,
 FOREIGN KEY (category_id) REFERENCES category (category_id) ON DELETE CASCADE
);

INSERT INTO pattern (pattern_name, category_id)
VALUES
('Футболка поло', 4),
('Футболка Дженни', 4),
('Классическая футболка', 4),
('Классическая рубашка', 3),
('Пляжная рубашка', 3),
('Юбка-карандаш', 5),
('Юбка-солнце', 5),
('Классические брюки', 1),
('Брюки бананы', 1),
('Брюки скинни', 1),
('Брюки карго', 1), 
('Платье-футляр', 2);

CREATE TABLE IF NOT EXISTS users (
 users_id INTEGER PRIMARY KEY AUTOINCREMENT,
 users_login VARCHAR(30),
 users_password VARCHAR(30)
);

INSERT INTO users (users_login, users_password)
VALUES
('srf_adlr','qwertyasdfg');
''')

# сохраняем информацию в базе данных
con.commit()