import pandas as pd


def is_correct_login_and_password(conn, login, password):
    try:
        return pd.read_sql('''
        SELECT users_role
        FROM users
        WHERE users_login = :login AND users_password = :password;
        ''', conn, params={"login": login, "password": password}).values[0][0]

    except IndexError:
        return "error"


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


def get_user_id(conn, login):
    try:
        return pd.read_sql('''SELECT users_id 
        FROM users
        WHERE users_login = :login
        ''', conn, params={"login": login}).values[0][0]
    except IndexError:
        return "error"


def registration(conn, login, password):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users(users_login,users_password,users_role) 
    VALUES (:login,:password,"user")
     ''', {"login": login,"password": password})
    conn.commit()
    return cur.lastrowid
