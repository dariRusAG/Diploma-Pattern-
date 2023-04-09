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

CREATE TABLE IF NOT EXISTS measure (
 measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
 measure_name VARCHAR(10),
 measure_full_name VARCHAR(50)
);

INSERT INTO measure (measure_name, measure_full_name)
VALUES
('ОПл', 'Обхват плеча'),
('ОТ', 'Обхват талии'),
('ОБ', 'Обхват бедер'),
('ОШ', 'Обхват шеи'),
('ДР', 'Длина рукава'),
('ДПдТ', 'Длина переда до талии'),
('ДСдТ', 'Длина спины до талии'), 
('ДИпС', 'Длина изделия по спинке'),
('ДПл', 'Длина плеча'),
('ШПр', 'Ширина проймы'),
('ШС', 'Ширина спины'),
('ШГ', 'Ширина груди'),
('ВПлПК', 'Высота плеча переда косая'),
('ВПлК', 'Высота плеча косая'),
('ГП', 'Глубина проймы'),
('ОЗ', 'Обхват запястья'),
('ОГ', 'Длина горловины'),
('ВБ', 'Высота бедер'),
('ДИ', 'Длина изделия'),
('ВГ', 'Высота груди');

CREATE TABLE IF NOT EXISTS pattern_measure (
 pattern_measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
 pattern_id INTEGER,
 measure_id INTEGER,
 FOREIGN KEY (pattern_id) REFERENCES pattern (pattern_id) ON DELETE CASCADE,
 FOREIGN KEY (measure_id) REFERENCES measure (measure_id) ON DELETE CASCADE
);

INSERT INTO pattern_measure (pattern_id, measure_id)
VALUES
(1, 1), (1, 2), (1, 3),
(2, 1), (2, 2), (2, 3),
(3, 1), (3, 2), (3, 3),
(4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
(5, 7), (5, 8),
(6, 10), (6, 11),
(7, 12),
(8, 13),
(9, 14), (9, 15),
(10, 14), (10, 15),
(11, 14), (11, 15), (11, 16),
(12, 17), (12, 18), (12, 19), (12, 20);

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
(4, 1, 28), (4, 2, 68), (4, 3, 94), (4, 4, 23), (4, 5, 48), 
(4, 6, 72), (4, 7, 75), (4, 8, 80), (4, 9, 56), (4, 10, 103), 
(4, 11, 132), (4, 12, 88), (4, 13, 97), (4, 14, 48), (4, 15, 14);

CREATE TABLE IF NOT EXISTS formula (
 formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
 formula_name VARCHAR(50),
 formula_value VARCHAR(100)
);

INSERT INTO formula (formula_name, formula_value)
VALUES
('ah', 'dlina_izd'),
('hh', '0.5 * obhvat_bed_1 + 1'),
('ab', 'dlina_izd - vusota_bed'),
('c', '0.5*obhvat_bed_1 - 0.5*obhvat_t'),
('bok_v', '0.5*(0.5*obhvat_bed_1 - 0.5*obhvat_t)'),
('tr', '0.5*(0.5 * obhvat_bed_1 + 1)-(0.5*(0.5*obhvat_bed_1 - 0.5*obhvat_t))*0.5');

CREATE TABLE IF NOT EXISTS line (
 line_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 x_first_coord varchar(70),
 y_first_coord varchar(70),
 x_second_coord varchar(70),
 y_second_coord varchar(70),
 line_type varchar(10),
 x_deviation REAL,
 y_deviation REAL,
 line_design varchar(15),
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE
);

INSERT INTO line (x_first_coord, y_first_coord, x_second_coord, y_second_coord, line_type, x_deviation, y_deviation, line_design)
VALUES
('1', 'ah', '1', '1', 'line','','','normal'),
('1', '1', '0.5*hh', '1', 'line','','','normal'),
('0.5*hh', '1', '0.5*hh', 'ab', 'line','','','normal'),
('0.5*hh', 'ab', '1', 'ab', 'line','','','normal'),
('1', 'ab', '0.5*hh', 'ab', 'line','','','dotted'),
('0.5*hh', 'ab', '0.5*hh', 'ah+1', 'line','','','dotted'),
('0.5*hh', 'ah+1','tr', 'ah+1', 'line','','','dotted'),
('0.5*hh', 'ah','1', 'ah', 'line','','','dotted'),
('0.25*hh', 'ab', '0.25*hh', 'ah', 'line','','','dotted'),
('0.25*hh', 'ah', '0.25*hh', 'ah-13', 'line','','','dotted'),
('0.25*hh', 'ah-13', '0.25*hh-2', 'ah+0.1', 'line','','','dotted'),
('0.25*hh-2', 'ah+0.1', '0.25*hh', 'ah-13', 'line','','','dotted'),
('0.25*hh', 'ah-13', '0.25*hh+2', 'ah+0.3', 'line','','','dotted'),
('tr', 'dlina_izd + 1', '0.5*hh', 'ab', 'curve', '1/4', '3/4', 'normal'),
('1', 'dlina_izd', 'tr', 'dlina_izd + 1', 'curve', '2/3', '4/5', 'normal');

CREATE TABLE IF NOT EXISTS detail (
 detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS detail_formula (
 detail_formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 formula_id INTEGER,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE,
 FOREIGN KEY (formula_id) REFERENCES formula (formula_id) ON DELETE CASCADE
);

''')

# сохраняем информацию в базе данных
con.commit()
