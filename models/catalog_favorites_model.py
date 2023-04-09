import pandas as pd


# Вывод всех категорий выкроек
def get_category(conn):
    return pd.read_sql('''
    SELECT category_name
    FROM category
    ORDER BY category_name
    ''', conn)


# Вывод всех выкроек
def get_pattern(conn, category, complexity):
    return pd.read_sql(f'''
    SELECT
        pattern_id AS ID,
        pattern_name AS Название, 
        category_name AS Категория,
        picture AS Изображение,
        complexity AS Сложность        
    FROM pattern
    JOIN category USING (category_id)
    WHERE (category_name IN ({str(category).strip('[]')}) OR {not category})
    AND (complexity IN ({str(complexity).strip('[]')}) OR {not complexity})
    GROUP BY pattern_id
    ORDER BY pattern_name
    ''', conn)


# Вывод всех избранных выкроек
def get_favorite_pattern(conn, user_id, category, complexity):
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
    WHERE (category_name IN ({str(category).strip('[]')}) OR {not category})
    AND (complexity IN ({str(complexity).strip('[]')}) OR {not complexity})
    GROUP BY pattern_id
    ORDER BY pattern_name
    ''', conn)


# Добавление выкройки в избранное
def add_pattern(conn, user_id, pattern_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO favorite(users_id, pattern_id) 
        VALUES (:user, :pattern)
    ''', {"user": user_id, "pattern": pattern_id})

    return conn.commit()


# Удаление выкройки из избранного
def del_pattern(conn, pattern_id):
    cur = conn.cursor()
    cur.execute(f'''
        DELETE FROM favorite
        WHERE pattern_id = :pattern;
     ''', {"pattern": pattern_id})

    return conn.commit()


