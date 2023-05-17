import pandas as pd


def get_category(conn):
    return pd.read_sql('''
    SELECT category_name, category_id
    FROM category
    ORDER BY category_name
    ''', conn)


def get_formula(conn):
    return pd.read_sql('''
    SELECT *
    FROM formula
    ORDER BY formula_name
    ''', conn)


def get_line(conn):
    return pd.read_sql('''
    SELECT x_first_coord, y_first_coord, x_second_coord, y_second_coord, x_deviation, y_deviation, line_design
    FROM line
    ''', conn)


def get_measure(conn):
    return pd.read_sql('''
    SELECT measure_name, measure_full_name
    FROM measure
    ORDER BY measure_name
    ''', conn)


def get_detail(conn):
    return pd.read_sql('''
    SELECT *
    FROM detail
    ORDER BY detail_name
    ''', conn)


def get_pattern(conn):
    return pd.read_sql('''
    SELECT pattern_id, pattern_name, category_name, picture, complexity, GROUP_CONCAT(detail_name) as detail_name
    FROM pattern
    LEFT JOIN category USING (category_id)
    LEFT JOIN pattern_detail USING (pattern_id)
    LEFT JOIN detail USING (detail_id)
    GROUP BY pattern_id
    ORDER BY pattern_name
    ''', conn)


def get_category_id(conn, category_name):
    try:
        return pd.read_sql('''SELECT category_id
        FROM category
        WHERE category_name = :category_name
        ''', conn, params={"category_name": category_name}).values[0][0]
    except IndexError:
        return "error"


def get_formula_id_by_value(conn, formula_name, formula_value):
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


def get_pattern_id(conn, pattern_name):
    try:
        return pd.read_sql('''SELECT pattern_id
        FROM pattern
        WHERE pattern_name = :pattern_name
        ''', conn, params={"pattern_name": pattern_name}).values[0][0]
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


def get_measure_number(conn, detail_id):
    return pd.read_sql('''
    SELECT COUNT(measure_id)
    FROM detail_measure
    WHERE detail_id = :detail_id
    GROUP BY detail_id
    ''', conn, params={"detail_id": detail_id}).values[0][0]


def get_detail_size(conn, detail_id):
    try:
        return pd.read_sql('''SELECT detail_size
          FROM detail
          WHERE detail_id = :detail_id
          ''', conn, params={"detail_id": detail_id}).values[0][0]
    except IndexError:
        return "error"


def get_detail_measure(conn, detail_id):
    try:
        return pd.read_sql('''SELECT measure_id,  measure_name, measure_full_name
          FROM detail_measure
          INNER JOIN measure USING (measure_id)
          WHERE detail_id = :detail_id
          ''', conn, params={"detail_id": detail_id})
    except IndexError:
        return "error"


def get_detail_formula(conn, detail_id):
    try:
        return pd.read_sql('''SELECT formula_name, formula_value
          FROM detail_formula
          INNER JOIN formula USING (formula_id)
          WHERE detail_id = :detail_id
          ''', conn, params={"detail_id": detail_id})
    except IndexError:
        return "error"


def get_detail_lines(conn, detail_id):
    try:
        return pd.read_sql('''SELECT x_first_coord, y_first_coord, x_second_coord, y_second_coord, x_deviation, y_deviation, line_design
          FROM line
          WHERE detail_id = :detail_id
          ''', conn, params={"detail_id": detail_id})
    except IndexError:
        return "error"



def get_detail_by_id(conn, pattern_id):
    try:
        return pd.read_sql('''SELECT GROUP_CONCAT(detail_name) as detail_name
          FROM pattern_detail
          JOIN detail USING (detail_id)
          WHERE pattern_id = :pattern_id
          GROUP BY pattern_id
          ''', conn, params={"pattern_id": pattern_id}).values[0][0]
    except IndexError:
        return "error"


def get_category_by_id(conn, category_id):
    try:
        return pd.read_sql('''SELECT category_name
          FROM category
          WHERE category_id = :category_id
          ''', conn, params={"category_id": category_id}).values[0][0]
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


def add_detail(conn, detail_name, detail_size):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO detail(detail_name, detail_size) 
    VALUES (:detail_name, :detail_size)
     ''', {"detail_name": detail_name, "detail_size": detail_size})
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
    INSERT INTO line(detail_id, x_first_coord, y_first_coord, x_second_coord, y_second_coord, x_deviation, y_deviation, line_design)
    VALUES (:detail_id, :x_first_coord, :y_first_coord, :x_second_coord, :y_second_coord, :x_deviation, :y_deviation, :line_design)
     ''', {"detail_id": detail_id, "x_first_coord": line[0], "y_first_coord": line[1], "x_second_coord": line[2],
           "y_second_coord": line[3], "x_deviation": line[4], "y_deviation": line[5],
           "line_design": line[6]})
    conn.commit()
    return cur.lastrowid


def add_pattern(conn, pattern_name, picture, category, complexity):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO pattern(pattern_name, category_id, picture, complexity) 
    VALUES (:pattern_name, :category, :picture, :complexity)
     ''', {"pattern_name": pattern_name, "picture": picture, "category": category, "complexity": complexity})
    conn.commit()
    return cur.lastrowid


def add_pattern_detail(conn, pattern_id, detail_id):
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO pattern_detail(pattern_id, detail_id) 
    VALUES (:pattern_id, :detail_id)
     ''', {"pattern_id": pattern_id, "detail_id": detail_id})
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


def delete_formula(conn, formula_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM formula
    WHERE formula_id=:formula_id;
     ''', {"formula_id": formula_id})
    conn.commit()
    return cur.lastrowid


def delete_detail(conn, detail_id, function_name):
    cur = conn.cursor()
    if function_name == 'Удаление':
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


def delete_pattern_detail(conn, pattern_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM pattern_detail
    WHERE pattern_id=:pattern_id;
     ''', {"pattern_id": pattern_id})
    conn.commit()
    return cur.lastrowid


def delete_pattern(conn, pattern_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM pattern
    WHERE pattern_id=:pattern_id;
     ''', {"pattern_id": pattern_id})
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


def update_formula(conn, formula_id, formula_name, formula_value):
    cur = conn.cursor()
    cur.execute('''
    UPDATE formula
    SET 
        formula_name= :formula_name,
        formula_value= :formula_value
    WHERE formula_id = :formula_id
    ''', {"formula_id": formula_id, "formula_name": formula_name, "formula_value": formula_value})
    return conn.commit()


def update_pattern(conn, pattern_id, pattern_name, pattern_picture, category_id, complexity):
    cur = conn.cursor()
    cur.execute('''
    UPDATE pattern
    SET 
        pattern_name= :pattern_name,
        picture= :pattern_picture,
        category_id= :category_id,
        complexity= :complexity
    WHERE pattern_id = :pattern_id
    ''', {"pattern_id": pattern_id, "pattern_name": pattern_name, "pattern_picture": pattern_picture, "category_id": category_id, "complexity": complexity})
    return conn.commit()

def update_detail(conn, detail_id, detail_name, detail_size):
    cur = conn.cursor()
    cur.execute('''
    UPDATE detail
    SET 
        detail_name= :detail_name,
        detail_size= :detail_size
    WHERE detail_id = :detail_id
    ''', {"detail_id": detail_id, "detail_name": detail_name, "detail_size": detail_size})
    return conn.commit()