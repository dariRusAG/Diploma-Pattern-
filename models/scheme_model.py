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
    SELECT 
    measure_name AS Обозначение, 
    measure_full_name AS Полное_название
    FROM measure 
    JOIN pattern_measure USING (measure_id)
    WHERE pattern_id == {index}
    ''', conn)


# Вывод параметров пользователя для построения
def get_param_user(conn, user_id):
    return pd.read_sql(f'''
    SELECT 
        param_name AS Обозначение, 
        user_param.[param_value] AS Значение
    FROM param
    JOIN user_param USING (param_id)
    WHERE users_id = {user_id}
    ''', conn)
