import pandas as pd


def get_favorite_pattern(conn, user_id):
    return pd.read_sql(f'''
    WITH get_favorite_id(pattern_id)
    AS(
        SELECT pattern_id
        FROM favorite 
        WHERE users_id == {user_id} 
    )
    SELECT
        pattern_id AS ID,
        pattern_name AS Название,
        category_name AS Категория, 
        picture AS Изображение,
        complexity AS Сложность       
    FROM pattern
    JOIN category USING (category_id)
    JOIN get_favorite_id USING (pattern_id)
    GROUP BY pattern_id
    ORDER BY pattern_name
    ''', conn)

