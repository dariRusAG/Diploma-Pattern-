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
('Лонгслив', 4, 3, '/static/image/picture_pattern/Лонгслив.jpg'),
('Классическая футболка', 4, 2, '/static/image/picture_pattern/Классическая%20футболка.jpg'),
('Классическая рубашка', 3, 4, '/static/image/picture_pattern/Классическая%20рубашка.jpg'),
('Пляжная рубашка', 3, 4, '/static/image/picture_pattern/Пляжная%20рубашка.jpg'),
('Юбка-карандаш', 5, 3, '/static/image/picture_pattern/Юбка-карандаш.jpg'),
('Юбка-солнце', 5, 1, '/static/image/picture_pattern/Юбка-солнце.jpg'),
('Классические брюки', 1, 4, '/static/image/picture_pattern/Классические%20брюки.jpg'),
('Брюки бананы', 1, 3, '/static/image/picture_pattern/Брюки%20бананы.jpg'),
('Брюки скинни', 1, 3, '/static/image/picture_pattern/Брюки%20скинни.jpg'),
('Брюки карго', 1, 4, '/static/image/picture_pattern/Брюки%20карго.jpg'),
('Платье-футляр', 2, 5, '/static/image/picture_pattern/Платье%20футляр.jpg');

CREATE TABLE IF NOT EXISTS detail (
 detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_name VARCHAR(50)
);

INSERT INTO detail (detail_name)
VALUES
('Передняя половина юбки-карандаш'),
('Задняя половина юбки-карандаш'),
('Основа верха'),
('Рукав');

CREATE TABLE IF NOT EXISTS pattern_detail (
 pattern_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
 pattern_id INTEGER,
 detail_id INTEGER,
 FOREIGN KEY (pattern_id) REFERENCES pattern (pattern_id) ON DELETE CASCADE,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE
);

INSERT INTO pattern_detail (pattern_id, detail_id)
VALUES
(6, 1), (6, 2),
(2, 3), (2, 4);

CREATE TABLE IF NOT EXISTS measure (
 measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
 measure_name VARCHAR(10),
 measure_full_name VARCHAR(50)
);

INSERT INTO measure (measure_name, measure_full_name)
VALUES
('ОГ', 'Обхват груди'),
('ОТ', 'Обхват талии'),
('ОБ', 'Обхват бедер'),
('ОШ', 'Обхват шеи'),
('ОПл', 'Обхват плеча'),
('ОЗ', 'Обхват запястья'),
('ВБ', 'Высота бедер'),
('ДИ', 'Длина изделия'),
('ДТС', 'Длина до талии спинки'),
('ДПл', 'Длина плеча'),
('ДР', 'Длина рукава');

CREATE TABLE IF NOT EXISTS detail_measure (
 detail_measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 measure_id INTEGER,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE,
 FOREIGN KEY (measure_id) REFERENCES measure (measure_id) ON DELETE CASCADE
);

INSERT INTO detail_measure (detail_id, measure_id)
VALUES
(1, 2), (1, 3), (1, 7), (1, 8),
(2, 2), (2, 3), (2, 7), (2, 8),
(3, 1), (3, 2), (3, 4), (3, 5), (3, 8), (3, 9),  (3, 10),
(4, 5), (4, 6), (4, 11);

CREATE TABLE IF NOT EXISTS formula (
 formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
 formula_name VARCHAR(50),
 formula_value VARCHAR(100)
);

INSERT INTO formula (formula_name, formula_value)
VALUES
('Длина', 'ДИ + 1'),
('Середина', 'ДИ - ВБ + 1'),
('Ширина', '0.25 * ОБ + 1.5'),
('Боковая_вытачка', '0.25 * (ОБ - ОТ)'),
('Вытачка_переда', 'ДИ - 0.5 * ВБ + 1'),
('Подъем_талии', 'ДИ + 1.5 + 1'),
('Ширина_верха', 'ОГ * 0.25 * 0.95 + 1'),
('Линия_талии', '0.25 * ОТ + 1.5'),
('Боковой_шов', 'ДИ - ДТС + 2'),
('Горловина', 'ОШ / 6 + 2'),
('Плечо', 'ДПл - 1.5'),
('Угол_проймы', '0.5 * (0.33 * ОПл + 0.5)'),
('Пройма', 'ДИ - (0.1 * ОГ + 10.5) + 1'),
('Высота_оката', '0.5 * ОПл + 1.5'),
('Длина_рукава', 'ДР + 1'),
('Низ_рукава', '0.5 * ОЗ + 2'),
('Линия_оката', 'ДР - 0.75 * (0.1 * ОГ + 10.5) + 3');

CREATE TABLE IF NOT EXISTS detail_formula (
 detail_formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 formula_id INTEGER,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE,
 FOREIGN KEY (formula_id) REFERENCES formula (formula_id) ON DELETE CASCADE
);

INSERT INTO detail_formula (detail_id, formula_id)
VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
(3, 1), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13),
(4, 14), (4, 15), (4, 16), (4, 17);

CREATE TABLE IF NOT EXISTS line_straight (
 line_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 x_first_coord varchar(70),
 y_first_coord varchar(70),
 x_second_coord varchar(70),
 y_second_coord varchar(70),
 line_design varchar(15),
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE
);

INSERT INTO line_straight (
    detail_id, 
    x_first_coord, y_first_coord, 
    x_second_coord, y_second_coord, 
    line_design)
VALUES
(1, '1', 'Длина', '1', '1', 'Обычная'),
(1, '1', '1', 'Ширина', '1', 'Обычная'),
(1, 'Ширина', '1', 'Ширина', 'Середина', 'Обычная'),
(1, '(Ширина - 1) * 0.5 - Боковая_вытачка * 0.6 * 0.5', 'Длина', 
'Ширина * 0.5', 'Длина - 2 * Боковая_вытачка', 'Обычная'),
(1, '(Ширина - 1) * 0.5 + Боковая_вытачка * 0.6 * 0.5', 'Длина', 
'Ширина * 0.5', 'Длина - 2 * Боковая_вытачка', 'Обычная'),
(2, 'Ширина', '1', '1', '1', 'Обычная'),
(2, 'Ширина', 'Длина', 'Ширина', '1', 'Обычная'),
(2, '1', '1', '1', 'Середина', 'Обычная'),
(2, '(Ширина - 1) * 0.5 - Боковая_вытачка * 0.4 * 0.5', 
'Длина', '(Ширина - 1) * 0.5 - 0.5',  'Вытачка_переда', 'Обычная'),
(2, '(Ширина - 1) * 0.5 + Боковая_вытачка * 0.4 * 0.5', 
'Длина', '(Ширина - 1) * 0.5 - 0.5',  'Вытачка_переда', 'Обычная'),
(3, '1', '1', 'Ширина_верха', '1', 'Обычная'),
(3, '1', 'Длина', '1', '1', 'Обычная'),
(3, 'Горловина', 'Длина + 2', 'Плечо', 'Длина - 1', 'Обычная'),
(4, 'Высота_оката', 'Длина_рукава', 'Высота_оката', '1', 'Обычная'),
(4, 'Высота_оката - Низ_рукава', '1', 'Высота_оката', '1', 'Обычная');

CREATE TABLE IF NOT EXISTS line_curve (
 line_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 x_first_coord varchar(70),
 y_first_coord varchar(70),
 x_second_coord varchar(70),
 y_second_coord varchar(70),
 line_design varchar(15),
 x_deviation varchar(70),
 y_deviation varchar(70),
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE
);

INSERT INTO line_curve (
    detail_id,
    x_first_coord, y_first_coord, 
    x_second_coord, y_second_coord,
    line_design, 
    x_deviation, y_deviation)
VALUES
(1, 'Ширина', 'Середина', 'Ширина - 0.5 * Боковая_вытачка', 'Подъем_талии', 'Обычная', '1.1', '1.1'),
(1, '1', 'Длина', 'Ширина - 0.5 * Боковая_вытачка', 'Подъем_талии', 'Обычная', '1.3', '0.98'),
(2, '1', 'Середина', '0.5 * Боковая_вытачка + 1', 'Подъем_талии', 'Обычная', '1.1', '1.1'),
(2, 'Ширина', 'Длина', '0.5 * Боковая_вытачка + 1', 'Подъем_талии', 'Обычная', '1.3', '1'),
(3, '1', 'Длина', 'Горловина', 'Длина + 2', 'Обычная', '1.4', '0.98'),
(3, 'Горловина', 'Длина + 2', '1', 'Длина + 1 - (Горловина - 2.5)', 'Обычная', '1.66', '0.95'),
(3, 'Плечо', 'Длина - 1', 'Ширина_верха', 'Пройма', 'Обычная', '0.65, 0.65', '0.88, 0.87'),
(3, 'Ширина_верха', 'Пройма', 'Ширина_верха', '1', 'Обычная', '0.84, 0.8, 0.86, 1.01', '0.9, 0.8, 0.8, 0.9'),
(4, '1', 'Линия_оката', 'Высота_оката - Низ_рукава', '1', 'Обычная', '1.5', '1.4'),
(4, 'Высота_оката', 'Длина_рукава', '1', 'Линия_оката', 'Обычная', '1, 1', '1.08, 0.94');

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
(4, 1), (4, 4), (4, 6), (4, 7), (4, 11),
(3, 2), (3, 5), (3, 12);

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
('ОГ', 'Обхват груди'),
('ДТП', 'Длина переда до талии'),
('ДТС', 'Длина спины до талии'), 
('ДПл', 'Длина плеча'),
('ШС', 'Ширина спины'),
('ШГ', 'Ширина груди'),
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
(4, 1, 34), (4, 2, 89), (4, 3, 94), (4, 4, 37), (4, 5, 108), 
(4, 6, 48), (4, 7, 45), (4, 8, 18), 
(4, 11, 17), (4, 12, 45), (4, 13, 32);
''')

# сохраняем информацию в базе данных
con.commit()

# (3, 'Ширина_верха', 'Пройма', 'Линия_талии', 'Боковой_шов', 'Обычная', '0.9', '1.01', '', ''),
# (3, 'Линия_талии', 'Боковой_шов', 'Ширина_верха', '1', 'Обычная', '1.35', '1.8', '0.75', '0.9'),
