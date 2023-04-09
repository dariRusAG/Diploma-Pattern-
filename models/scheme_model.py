import pandas as pd


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


def get_measure_pattern(conn, index):
    return pd.read_sql(f'''
    SELECT 
    measure_name AS Обозначение, 
    measure_full_name AS Полное_название
    FROM measure 
    JOIN pattern_measure USING (measure_id)
    WHERE pattern_id == {index}
    ''', conn)
