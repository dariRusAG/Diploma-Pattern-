import pandas


# Выбираем и выводим все данные пользователя
def get_data_user(conn, user_id):
    return pandas.read_sql(f'''
    SELECT 
        users_login AS Логин, 
        users_password AS Пароль
    FROM users 
    WHERE users_id = {user_id}
    ''', conn)


def get_param_user(conn, user_id):
    return pandas.read_sql(f'''
    SELECT param_name, param_full_name, user_param.[user_param_value]
    FROM param 
    INNER JOIN user_param ON param.param_id = user_param.param_id
    WHERE users_id = {user_id}
    ''', conn)


def update_data_user(conn, user_id, new_data_user):
    cur = conn.cursor()
    cur.execute('''
    UPDATE users
    SET 
        users_login = :login,
        users_password = :password
    WHERE users_id = :user_id
    ''', {"user_id": user_id, "login": new_data_user[0], "password": new_data_user[1]})

    return conn.commit()


def update_param_user(conn, user_id, elem, new_param_user):
    cur = conn.cursor()
    cur.execute('''
    UPDATE user_param
    SET user_param_value = :new_param_user
    WHERE (users_id = :user_id) AND (param_id = :elem)
    ''', {"user_id": user_id, "new_param_user": new_param_user, "elem": elem})

    return conn.commit()


def get_param(conn, user_id):
    return pandas.read_sql(f'''
    SELECT param_name
    FROM param 
    INNER JOIN user_param ON param.param_id = user_param.param_id
    WHERE users_id = {user_id}
    ''', conn)

def get_param_id(conn, param_name):
    try:
        return pandas.read_sql('''SELECT param_id
        FROM param
        WHERE param_name = :param_name
        ''', conn, params={"param_name": param_name}).values[0][0]
    except IndexError:
        return "error"


def is_correct_user_data(conn, login):
    try:
        return pandas.read_sql('''
        SELECT users_role
        FROM users
        WHERE users_login = :login
        ''', conn, params={"login": login}).values[0][0]

    except IndexError:
        return "error"