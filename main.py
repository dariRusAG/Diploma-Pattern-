import sqlite3

con = sqlite3.connect("DB.sqlite")

con.executescript('''
CREATE TABLE IF NOT EXISTS category (
 category_id INTEGER PRIMARY KEY AUTOINCREMENT,
 category_name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS pattern (
 pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
 pattern_name VARCHAR(70),
 complexity INTEGER,
 picture VARCHAR(70),
 category_id INTEGER,
 FOREIGN KEY (category_id) REFERENCES category (category_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detail (
 detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_name VARCHAR(50),
 detail_size VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS pattern_detail (
 pattern_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
 pattern_id INTEGER,
 detail_id INTEGER,
 FOREIGN KEY (pattern_id) REFERENCES pattern (pattern_id) ON DELETE CASCADE,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS measure (
 measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
 measure_name VARCHAR(10),
 measure_full_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS detail_measure (
 detail_measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 measure_id INTEGER,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE,
 FOREIGN KEY (measure_id) REFERENCES measure (measure_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS formula (
 formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
 formula_name VARCHAR(50),
 formula_value VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS detail_formula (
 detail_formula_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 formula_id INTEGER,
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE,
 FOREIGN KEY (formula_id) REFERENCES formula (formula_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS line (
 line_id INTEGER PRIMARY KEY AUTOINCREMENT,
 detail_id INTEGER,
 x_first_coord varchar(70), y_first_coord varchar(70),
 x_second_coord varchar(70), y_second_coord varchar(70),
 line_design varchar(15),
 x_deviation varchar(70), y_deviation varchar(70),
 FOREIGN KEY (detail_id) REFERENCES detail (detail_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
 users_id INTEGER PRIMARY KEY AUTOINCREMENT,
 users_login VARCHAR(30),
 users_password VARCHAR(30),
 users_role VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS favorite (
 favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
 users_id INTEGER,
 pattern_id INTEGER,
 FOREIGN KEY (users_id) REFERENCES users (users_id) ON DELETE CASCADE,
 FOREIGN KEY (pattern_id) REFERENCES pattern (pattern_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS param (
 param_id INTEGER PRIMARY KEY AUTOINCREMENT,
 param_name VARCHAR(10),
 param_full_name VARCHAR(50),
 param_value_w VARCHAR(70),
 param_value_m VARCHAR(70)
);

CREATE TABLE IF NOT EXISTS user_param (
 user_param_id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_param_value INTEGER,
 users_id INTEGER,
 param_id INTEGER,
 FOREIGN KEY (users_id) REFERENCES users (users_id) ON DELETE CASCADE,
 FOREIGN KEY (param_id) REFERENCES param (param_id) ON DELETE CASCADE
);
''')


con.executescript('''
INSERT INTO category (category_name)
VALUES
('Брюки'),
('Платья'),
('Рубашки'),
('Футболки'),
('Юбки');

INSERT INTO pattern (pattern_name, category_id, complexity, picture)
VALUES
('Футболка поло', 4, 2, '/static/image/picture_pattern/Футболка%20поло.jpg'),
('Лонгслив', 4, 1, '/static/image/picture_pattern/Лонгслив.jpg'),
('Классическая футболка', 4, 1, '/static/image/picture_pattern/Классическая%20футболка.jpg'),
('Классическая рубашка', 3, 3, '/static/image/picture_pattern/Классическая%20рубашка.jpg'),
('Пляжная рубашка', 3, 4, '/static/image/picture_pattern/Пляжная%20рубашка.jpg'),
('Юбка-карандаш', 5, 1, '/static/image/picture_pattern/Юбка-карандаш.jpg'),
('Юбка-солнце', 5, 1, '/static/image/picture_pattern/Юбка-солнце.jpg'),
('Классические брюки', 1, 2, '/static/image/picture_pattern/Классические%20брюки.jpg'),
('Брюки бананы', 1, 3, '/static/image/picture_pattern/Брюки%20бананы.jpg'),
('Брюки скинни', 1, 3, '/static/image/picture_pattern/Брюки%20скинни.jpg'),
('Брюки карго', 1, 4, '/static/image/picture_pattern/Брюки%20карго.jpg'),
('Платье-футляр', 2, 5, '/static/image/picture_pattern/Платье%20футляр.jpg');

INSERT INTO pattern_detail (pattern_id, detail_id)
VALUES
(6, 1), (6, 2),
(2, 3), (2, 4),
(1, 3), (1, 5), (1, 6);

INSERT INTO detail (detail_name, detail_size)
VALUES
('Передняя половина юбки-карандаш', 'ДН'),
('Задняя половина юбки-карандаш', 'ДН'),
('Основа верха', 'ДВ'),
('Длинный рукав', 'ДР'),
('Короткий рукав', ''),
('Воротник', ''),
('Карман', ''),
('Передняя половина платья-футляр', 'ДТ');

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
('ДР', 'Длина рукава'),
('ДЛ', 'Длина руки до локтя');

INSERT INTO detail_measure (detail_id, measure_id)
VALUES
(1, 2), (1, 3), (1, 7), (1, 8),
(2, 2), (2, 3), (2, 7), (2, 8),
(3, 1), (3, 2), (3, 4), (3, 5), (3, 8), (3, 9),  (3, 10),
(4, 1), (4, 5), (4, 6), (4, 11),
(5, 1), (5, 5), (5, 12),
(6, 1), (6, 4);

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
('Линия_оката', 'ДР - 0.75 * (0.1 * ОГ + 10.5) + 3'),
('Половина_длины_горловины', '0.1 * 0.25 * ОГ + 3.14 * 0.5 * (ОШ / 6 + 1.5) + 1'),
('Длина_короткого_рукава', 'ДЛ * 0.5 + 1'),
('Линия_оката_короткого_рукава', 'ДЛ * 0.5 - 0.75 * (0.1 * ОГ + 10.5) + 1.5');

INSERT INTO detail_formula (detail_id, formula_id)
VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
(3, 1), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13),
(4, 14), (4, 15), (4, 16), (4, 17),
(5, 14), (5, 17), (5, 19), (5, 20),
(6, 18);

INSERT INTO line (
    detail_id,
    x_first_coord, y_first_coord, 
    x_second_coord, y_second_coord,
    line_design, 
    x_deviation, y_deviation)
VALUES
(1, '1', 'Длина', '1', '1', 'Обычная', '', ''),
(1, '1', '1', 'Ширина', '1', 'Обычная', '', ''),
(1, 'Ширина', '1', 'Ширина', 'Середина', 'Обычная', '', ''),
(1, '(Ширина - 1) * 0.5 - Боковая_вытачка * 0.6 * 0.5', 'Длина', 'Ширина * 0.5', 'Длина - 2 * Боковая_вытачка', 
'Обычная', '', ''),
(1, '(Ширина - 1) * 0.5 + Боковая_вытачка * 0.6 * 0.5', 'Длина + 0.1', 'Ширина * 0.5', 'Длина - 2 * Боковая_вытачка', 
'Обычная', '', ''),
(1, 'Ширина', 'Середина', 'Ширина - 0.5 * Боковая_вытачка', 'Подъем_талии', 'Обычная', '1.1', '1.1'),
(1, '1', 'Длина', 'Ширина - 0.5 * Боковая_вытачка', 'Подъем_талии', 'Обычная', '1.3', '0.98'),

(2, 'Ширина', '1', '1', '1', 'Обычная', '', ''),
(2, 'Ширина', 'Длина', 'Ширина', '1', 'Обычная', '', ''),
(2, '1', '1', '1', 'Середина', 'Обычная', '', ''),
(2, '(Ширина - 1) * 0.5 - Боковая_вытачка * 0.4 * 0.5', 'Длина + 0.2', '(Ширина - 1) * 0.5 - 0.5',
 'Вытачка_переда', 'Обычная', '', ''),
(2, '(Ширина - 1) * 0.5 + Боковая_вытачка * 0.4 * 0.5', 'Длина', '(Ширина - 1) * 0.5 - 0.5',  'Вытачка_переда', 
'Обычная', '', ''),
(2, '1', 'Середина', '0.5 * Боковая_вытачка + 1', 'Подъем_талии', 'Обычная', '0.3', '1.1'),
(2, 'Ширина', 'Длина', '0.5 * Боковая_вытачка + 1', 'Подъем_талии', 'Обычная', '0.7', '0.98'),

(3, '1', '1', 'Ширина_верха', '1', 'Обычная', '', ''),
(3, '1', 'Длина', '1', '1', 'Обычная', '', ''),
(3, 'Горловина', 'Длина + 2', 'Плечо', 'Длина - 1', 'Обычная', '', ''),
(3, '1', 'Длина', 'Горловина', 'Длина + 2', 'Обычная', '1.4', '0.98'),
(3, 'Горловина', 'Длина + 2', '1', 'Длина + 1 - (Горловина - 2.5)', 'Обычная', '1.66', '0.95'),
(3, 'Плечо', 'Длина - 1', 'Ширина_верха', 'Пройма', 'Обычная', '0.65, 0.65', '0.88, 0.87'),
(3, 'Ширина_верха', 'Пройма', 'Ширина_верха', '1', 'Обычная', '0.84, 0.8, 0.86, 1.01', '0.9, 0.8, 0.8, 0.9'),

(4, 'Высота_оката', 'Длина_рукава', 'Высота_оката', '1', 'Обычная', '', ''),
(4, 'Высота_оката - Низ_рукава', '1', 'Высота_оката', '1', 'Обычная', '', ''),
(4, '1', 'Линия_оката', 'Высота_оката - Низ_рукава', '1', 'Обычная', '1.5', '1.4'),
(4, 'Высота_оката', 'Длина_рукава', '1', 'Линия_оката', 'Обычная', '1, 1', '1.08, 0.94'),

(5, 'Высота_оката + 1.5', 'Длина_короткого_рукава + 0.5', '1', 'Линия_оката_короткого_рукава', 'Обычная', '0.75, 0.5, 1.4', '1.25, 1.15, 0.6'),
(5, 'Высота_оката + 1.5', 'Длина_короткого_рукава + 0.5', 'Высота_оката * 2 + 0.5 + 1', 'Линия_оката_короткого_рукава', 'Обычная', '1.1, 1.11, 0.9', '1.2, 1.1, 0.6'),
(5, '1', '1', 'Высота_оката * 2 + 0.5 + 1', '1', 'Обычная', '1', '2'),
(5, '1', 'Линия_оката_короткого_рукава', '1', '1', 'Обычная', '', ''),
(5, 'Высота_оката * 2 + 0.5 + 1', 'Линия_оката_короткого_рукава', 'Высота_оката * 2 + 0.5 + 1', '1', 'Обычная', '', ''),

(6, '1', '1', '1', '4', 'Обычная', '', ''),
(6, '1', '4', 'Половина_длины_горловины * 0.5 + 1', '4', 'Обычная', '', ''),
(6, '1', '1', 'Половина_длины_горловины * 0.5 + 1', '1', 'Обычная', '', ''),
(6, 'Половина_длины_горловины * 0.5 + 1', '4', 'Половина_длины_горловины - 0.5', '4.5', 'Обычная', '1, 1', '0.95, 0.98'),
(6, 'Половина_длины_горловины * 0.5 + 1', '1', 'Половина_длины_горловины + 1.5', '1.5', 'Обычная', '1, 1', '0.85, 0.95'),
(6, 'Половина_длины_горловины - 0.5', '4.5', 'Половина_длины_горловины + 1.5', '1.5', 'Обычная', '1.04, 1.08, 1.05, 1.025', '1.2, 1.24, 1.05, 1'),

(6, '1', '11', '1', '6', 'Обычная', '', ''),
(6, '1', '6', 'Половина_длины_горловины - 0.5', '4.5', 'Обычная', '1, 1, 1.05, 1.05', '1.03, 1.1, 1.2, 1.14'),
(6, '1', '11', 'Половина_длины_горловины + 0.5', '13', 'Обычная', '1, 1, 1, 1', '0.97, 0.92, 0.95, 0.97'),
(6, 'Половина_длины_горловины + 0.5', '13', 'Половина_длины_горловины - 0.5', '4.5', 'Обычная', '', '');

INSERT INTO users (users_login, users_password, users_role)
VALUES
('nakao.pd','1234567','admin'),
('srf_adlr','qwerty','admin'),
('burakov.aa','burpass','user'),
('test','test','user');

INSERT INTO param (param_name, param_full_name, param_value_w, param_value_m)
VALUES
('ОГ', 'Обхват груди', '84, 88, 92, 96, 100, 104', '88, 92, 96, 100, 104, 108'),
('ОТ', 'Обхват талии', '65.5, 67.3, 71.3, 75.5, 80, 84.1', '76, 79, 82, 84, 91, 98'),
('ОБ', 'Обхват бедер', '96.3, 96.5, 99.8, 103.2, 106.7, 110.2', '93.8, 96, 98.3, 101.7, 104, 109.5'),
('ОШ', 'Обхват шеи', '35.5, 35.9, 36.6, 37.3, 38, 38.8', '39.2, 39.8, 40.5, 41.2, 42.1, 43.2'),
('ОПл', 'Обхват плеча', '26.8, 27.6, 29.1, 30.5, 31.8, 33', '28.3, 29.3, 30.2, 32.3, 33.8, 34.7'),
('ОЗ', 'Обхват запястья', '16, 16.1, 16.4, 16.7, 17.0, 17.2', '17.7, 18, 18.3, 18.6, 19, 19.3'),
('ВБ', 'Высота бедер', '20.8, 21, 21.2, 21.4, 21.5, 21.7', '19.2, 19.6, 20, 20.4, 20.7, 21'),
('ДТС', 'Длина до талии спинки', '41.2, 41.3, 41.4, 41.4, 41.5, 41.6', '45.8, 46, 46.3, 46.4, 46.5, 47'),
('ДТП', 'Длина до талии переда', '43, 43.8, 44.4, 44.9, 45.4, 46', '46.4, 47, 47.5, 48, 48.5, 49.3'),
('ДПл', 'Длина плеча', '13.5, 13.5, 13.6, 13.6, 13.7, 13.8', '14.4, 14.6, 14.8, 15, 15.2, 15.4'),
('ДЛ', 'Длина руки до локтя', '33.3, 34, 34.7, 35.4, 36.1, 36.8', '34.8, 35.5, 36.2, 36.9, 37.6, 39.3'),
('ДР', 'Длина рукава', '60, 61, 62.1, 63.2, 64.3, 65.4', '63, 63.5, 63.8, 64, 64.5, 65'),
('ДВ', 'Длина верха', '68.7, 70, 71.3, 72.6, 73.9, 75.2', '74, 75, 76.4, 77.8, 78.7, 79.8'),
('ДН', 'Короткий низ', '59, 60, 61, 62, 63, 64', '61, 62, 63, 64, 65, 66'),
('ДТ', 'Длинный низ', '59, 60, 61, 62, 63, 64', '58.2, 59.3, 60.4, 61.5, 62.6, 63.7');

INSERT INTO favorite (users_id, pattern_id)
VALUES
(4, 1), (4, 4), (4, 6), (4, 7), (4, 11),
(3, 2), (3, 5), (3, 12);

INSERT INTO user_param (users_id, param_id, user_param_value)
VALUES
(4, 1, 108), 
(4, 2, 80), 
(4, 3, 105), 
(4, 4, 37), 
(4, 5, 30), 
(4, 6, 16), 
(4, 7, 21), 
(4, 8, 42), 
(4, 9, 44), 
(4, 10, 13), 
(4, 11, 35);
''')

# сохраняем информацию в базе данных
con.commit()
