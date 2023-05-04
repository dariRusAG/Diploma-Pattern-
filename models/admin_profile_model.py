import pandas as pd


def get_category(conn):
    return pd.read_sql('''
    SELECT category_name, category_id
    FROM category
    ORDER BY category_name
    ''', conn)


def get_formula(conn):
    return pd.read_sql('''
    SELECT formula_name, formula_value
    FROM formula
    ''', conn)


def get_line(conn):
    return pd.read_sql('''
    SELECT x_first_coord, y_first_coord, x_second_coord, y_second_coord, line_type, x_deviation, y_deviation, line_design
    FROM line
    ''', conn)


def get_measure(conn):
    return pd.read_sql('''
    SELECT measure_name, measure_full_name
    FROM measure
    ORDER BY measure_name
    ''', conn)


def get_category_id(conn, category_name):
    try:
        return pd.read_sql('''SELECT category_id
        FROM category
        WHERE category_name = :category_name
        ''', conn, params={"category_name": category_name}).values[0][0]
    except IndexError:
        return "error"


def get_formula_id(conn, formula_name, formula_value):
    try:
        return pd.read_sql('''SELECT formula_id
        FROM formula
        WHERE formula_name = :formula_name OR formula_value = :formula_value
        ''', conn, params={"formula_name": formula_name, "formula_value": formula_value}).values[0][0]
    except IndexError:
        return "error"


def get_detail_id(conn, detail_name):
    try:
        return pd.read_sql('''SELECT detail_id
        FROM detail
        WHERE detail_name = :detail_name
        ''', conn, params={"detail_name": detail_name}).values[0][0]
    except IndexError:
        return "error"


def get_formula_id(conn, formula_name):
    try:
        return pd.read_sql('''SELECT formula_id
        FROM formula
        WHERE formula_name = :formula_name
        ''', conn, params={"formula_name": formula_name}).values[0][0]
    except IndexError:
        return "error"


def get_measure_id(conn, measure_name):
    try:
        return pd.read_sql('''SELECT measure_id
          FROM measure
          WHERE measure_name = :measure_name
          ''', conn, params={"measure_name": measure_name}).values[0][0]
    except IndexError:
        return "error"


def add_formula(conn, formula_name, formula_value):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO formula (formula_name, formula_value)
    VALUES (:formula_name, :formula_value)
     ''', {"formula_name": formula_name, "formula_value": formula_value})
    conn.commit()
    return cur.lastrowid


def add_category(conn, category):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO category(category_name) 
    VALUES (:category)
     ''', {"category": category})
    conn.commit()
    return cur.lastrowid


def add_detail(conn, detail_name):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO detail(detail_name) 
    VALUES (:detail_name)
     ''', {"detail_name": detail_name})
    conn.commit()
    return cur.lastrowid


def add_detail_formula(conn, detail_id, formula_id):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO detail_formula(detail_id, formula_id) 
    VALUES (:detail_id, :formula_id)
     ''', {"detail_id": detail_id, "formula_id": formula_id})
    conn.commit()
    return cur.lastrowid


def add_detail_measure(conn, detail_id, measure_id):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO detail_measure(detail_id, measure_id) 
    VALUES (:detail_id, :measure_id)
     ''', {"detail_id": detail_id, "measure_id": measure_id})
    conn.commit()
    return cur.lastrowid


def add_detail_line(conn, detail_id, line):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO line(detail_id, x_first_coord, y_first_coord, x_second_coord, y_second_coord, line_type, x_deviation, y_deviation, line_design)
    VALUES (:detail_id, :x_first_coord, :y_first_coord, :x_second_coord, :y_second_coord, :line_type, :x_deviation, :y_deviation, :line_design)
     ''', {"detail_id": detail_id, "x_first_coord": line[1], "y_first_coord": line[2], "x_second_coord": line[3],
           "y_second_coord": line[4], "line_type": line[5], "x_deviation": line[6], "y_deviation": line[7],
           "line_design": line[8]})
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


def get_detail(conn):
    return pd.read_sql('''
    SELECT *
    FROM detail
    ''', conn)


def get_detail_f(conn):
    return pd.read_sql('''
    SELECT *
    FROM  detail_formula
    ''', conn)


def get_detail_m(conn):
    return pd.read_sql('''
    SELECT *
    FROM  detail_measure
    ''', conn)


def delete_new_detail(conn, detail_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM detail
    WHERE detail_id=:detail_id;
     ''', {"detail_id": detail_id})

    cur.execute(f'''
    DELETE FROM detail_measure
    WHERE detail_id=:detail_id;
     ''', {"detail_id": detail_id})

    cur.execute(f'''
    DELETE FROM detail_formula
    WHERE detail_id=:detail_id;
     ''', {"detail_id": detail_id})

    cur.execute(f'''
        DELETE FROM line
        WHERE detail_id=:detail_id;
         ''', {"detail_id": detail_id})
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
