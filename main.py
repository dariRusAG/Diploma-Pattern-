import sqlite3

con = sqlite3.connect("DB2.sqlite")

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
 complexity INTEGER,
 picture VARCHAR(70),
 category_id INTEGER,
 FOREIGN KEY (category_id) REFERENCES category (category_id) ON DELETE CASCADE
);

INSERT INTO pattern (pattern_name, category_id, complexity, picture)
VALUES
('Футболка поло', 4, 3, '/static/image/picture_pattern/Футболка%20поло.jpg'),
('Футболка Дженни', 4, 3, ''),
('Классическая футболка', 4, 2, '/static/image/picture_pattern/Классическая%20футболка.jpg'),
('Классическая рубашка', 3, 4, '/static/image/picture_pattern/Классическая%20рубашка.jpg'),
('Пляжная рубашка', 3, 4, ''),
('Юбка-карандаш', 5, 3, ''),
('Юбка-солнце', 5, 1, '/static/image/picture_pattern/Юбка-солнце.jpg'),
('Классические брюки', 1, 4, ''),
('Брюки бананы', 1, 3, '/static/image/picture_pattern/Брюки%20бананы.jpg'),
('Брюки скинни', 1, 3, ''),
('Брюки карго', 1, 4, '/static/image/picture_pattern/Брюки%20карго.jpg'),
('Платье-футляр', 2, 5, '');

CREATE TABLE IF NOT EXISTS users (
 users_id INTEGER PRIMARY KEY AUTOINCREMENT,
 users_login VARCHAR(30),
 users_password VARCHAR(30),
 users_role VARCHAR(10)
);

INSERT INTO users (users_login, users_password, users_role)
VALUES
('nakao.pd','1234567','admin'),
('srf_adlr','qwerty','admin'),
('burakov.aa','burpass','user'),
('test','test','user');

CREATE TABLE IF NOT EXISTS favorite (
 favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
 users_id INTEGER,
 pattern_id INTEGER,
 FOREIGN KEY (users_id) REFERENCES users (users_id) ON DELETE CASCADE,
 FOREIGN KEY (pattern_id) REFERENCES pattern (pattern_id) ON DELETE CASCADE
);

INSERT INTO favorite (users_id, pattern_id)
VALUES
(4,1), (4,4), (4,6), (4,7), (4,11),
(3,2), (3,5), (3,12);

CREATE TABLE IF NOT EXISTS param (
 param_id INTEGER PRIMARY KEY AUTOINCREMENT,
 param_name VARCHAR(10),
 param_full_name VARCHAR(50),
 param_value INTEGER
);

INSERT INTO param (param_name, param_full_name)
VALUES
('ОПл', 'Обхват плеча'),
('ОТ', 'Обхват талии'),
('ОБ', 'Обхват бедер'),
('ОШ', 'Обхват шеи'),
('ДПдТ', 'Длина переда до талии'),
('ДСдТ', 'Длина спины до талии'), 
('ДПл', 'Длина плеча'),
('ШПр', 'Ширина проймы'),
('ШС', 'Ширина спины'),
('ШГ', 'Ширина груди'),
('ВПлПК', 'Высота плеча переда косая'),
('ВПлК', 'Высота плеча косая'),
('ОЗ', 'Обхват запястья'),
('ВБ', 'Высота бедер'),
('ВГ', 'Высота груди');

CREATE TABLE IF NOT EXISTS user_param (
 user_param_id INTEGER PRIMARY KEY AUTOINCREMENT,
 param_value INTEGER,
 users_id INTEGER,
 param_id INTEGER,
 FOREIGN KEY (users_id) REFERENCES users (users_id) ON DELETE CASCADE,
 FOREIGN KEY (param_id) REFERENCES param (param_id) ON DELETE CASCADE
);

INSERT INTO user_param (users_id, param_id, param_value)
VALUES
(3, 1, 28), (3, 2, 68), (3, 3, 94), (3, 4, 23), (3, 5, 48), 
(3, 6, 72), (3, 7, 75), (3, 8, 80), (3, 9, 56), (3, 10, 103), 
(3, 11, 132), (3, 12, 88), (3, 13, 97), (3, 14, 48), (3, 15, 14);
''')

# сохраняем информацию в базе данных
con.commit()
