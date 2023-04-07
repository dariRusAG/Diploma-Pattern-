import pandas as pd


def get_category(conn):
    return pd.read_sql('''
    SELECT category_name, category_id
    FROM category
    ORDER BY category_name
    ''', conn)


def add_category(conn, category):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO category(category_name) 
    VALUES (:category)
     ''', {"category": category})
    conn.commit()
    return cur.lastrowid


def delete_category(conn, category_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM category
    WHERE category_id=:category_id;
     ''', {"category_id": category_id})
    conn.commit()
    return cur.lastrowid


def update_category(conn, category_id, category_name):
    cur = conn.cursor()
    cur.execute('''
    UPDATE category
    SET 
        category_name= :category_name
    WHERE category_id = :category_id
    ''', {"category_id": category_id, "category_name": category_name})
    return conn.commit()




def get_formula(conn):
    return pd.read_sql('''
    SELECT formula_name, formula_value
    FROM formula
    ''', conn)

def get_line(conn):
    return pd.read_sql('''
    SELECT x_first_coord, y_first_coord, x_second_coord, y_second_coord, line_design
    FROM line
    ''', conn)
