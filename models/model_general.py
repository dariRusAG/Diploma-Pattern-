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
    INSERT INTO users(users_login, users_password, users_role) 
    VALUES (:login,:password,"user")
     ''', {"login": login, "password": password})
    conn.commit()
    return cur.lastrowid


def new_user_params(conn, users_id):
    cur = conn.cursor()
    data = pd.read_sql(f'''
           SELECT param_id
           FROM param
           ''', conn)
    for param_id in range(1, len(data)):
        cur.execute('''
        INSERT INTO user_param(users_id, param_id, user_param_value) 
        VALUES (:users_id, :param_id, '')
        ''', {"users_id": users_id, "param_id": param_id})
        conn.commit()
    return cur.lastrowid


def to_delete_user(conn, user_id):
    cur = conn.cursor()
    cur.execute(f'''
    DELETE FROM users
    WHERE users_id = :user_id;
     ''', {"user_id": user_id})
    conn.commit()
    return cur.lastrowid

def get_detail_name(conn, detail_id):
        return pd.read_sql('''
        SELECT detail_name
        FROM detail
        WHERE detail_id = :detail_id
        ''', conn, params={"detail_id": detail_id}).values[0][0]

def get_params_max_min(conn, name):
    return pd.read_sql('''
            SELECT min_value, max_value
            FROM param
            WHERE param_name = :param_name
            ''', conn, params={"param_name": name}).values[0]