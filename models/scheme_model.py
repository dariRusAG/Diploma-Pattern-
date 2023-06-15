import pandas as pd


# Вывод данных выкройки для построения
def get_scheme_pattern(conn, index):
    return pd.read_sql(f'''
    SELECT
        pattern_id AS ID,
        pattern_name AS Название, 
        category_name AS Категория,
        picture AS Изображение  
    FROM pattern
    JOIN category USING (category_id)
    WHERE pattern_id == {index}
    ''', conn)


# Вывод всех мерок выкройки
def get_measure_pattern(conn, index):
    return pd.read_sql(f'''
    WITH get_all_measure(detail_id, measure_name, measure_full_name)
    AS (
        SELECT 
            detail_id, 
            group_concat(measure_name, ',') AS measure_name,
            group_concat(measure_full_name, ',') AS measure_full_name
        FROM detail_measure 
        JOIN measure USING (measure_id)
        GROUP BY detail_id
    )
    SELECT 
        detail_id AS ID,
        detail_name AS Название_детали,
        detail_size AS Длина_детали,
        measure_name AS Обозначение,
        measure_full_name AS Полное_название
    FROM pattern_detail 
    JOIN get_all_measure USING (detail_id) 
    JOIN detail USING (detail_id) 
    WHERE pattern_id == {index}
    ''', conn)

def get_measure_detail(conn, index):
    return pd.read_sql(f'''
    SELECT
        detail_id AS ID,
        measure_name AS Обозначение,
        measure_full_name AS Полное_название
    FROM detail_measure
    JOIN measure USING(measure_id)
    JOIN detail USING (detail_id)
    WHERE detail_id == {index}
    ''', conn)

def get_detail_no_measure(conn, index, list_detail):
    return pd.read_sql(f'''
    SELECT
        detail_id AS ID,
        '' AS Обозначение,
        '' AS Значение
    FROM pattern_detail
    WHERE pattern_id == {index} AND detail_id NOT IN ({str(list_detail).strip('[]')})
    ''', conn)

def get_info_param(conn):
    return pd.read_sql(f'''
        SELECT 
            param_name AS Обозначение, 
            info_param AS Информация_о_параметрах,
            info_picture AS Изображение
        FROM param
        ''', conn)

# Вывод параметров пользователя для построения
def get_param_user(conn, user_id):
    return pd.read_sql(f'''
    SELECT 
        param_name AS Обозначение, 
        user_param.[user_param_value] AS Значение
    FROM param
    JOIN user_param USING (param_id)
    WHERE users_id = {user_id}
    ''', conn)

# Вывод стандартных параметров женской фигуры
def get_param_standard_w(conn):
    return pd.read_sql('''
        SELECT 
            param_name AS Обозначение, 
            param_value_w AS Значение
        FROM param
        WHERE Обозначение != 'ДИ'
        ''', conn)

# Вывод стандартных параметров мужской фигуры
def get_param_standard_m(conn):
    return pd.read_sql('''
        SELECT 
            param_name AS Обозначение, 
            param_value_m AS Значение
        FROM param
        WHERE Обозначение != 'ДИ'
        ''', conn)

# Вывод формул детали
def get_formula_detail(conn, detail):
    return pd.read_sql(f'''
    SELECT 
        formula_name, 
        formula_value
    FROM formula
    JOIN detail_formula USING (formula_id)
    WHERE detail_id = {detail}
    ''', conn)


# Вывод линий детали
def get_line_detail(conn, detail):
    return pd.read_sql(f'''
    SELECT 
        detail_id,
        x_first_coord, y_first_coord, 
        x_second_coord, y_second_coord,
        x_deviation, y_deviation
    FROM line
    WHERE detail_id = {detail}
    ''', conn)
