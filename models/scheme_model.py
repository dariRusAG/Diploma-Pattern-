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
