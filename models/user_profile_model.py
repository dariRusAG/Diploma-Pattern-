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
    SELECT param_name, param_full_name, user_param.[param_value]
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
    SET param_value = :param
    WHERE (users_id = :user_id) AND (param_id = :i)
    ''', {"user_id": user_id, "param": new_param_user[elem], "i": elem + 1})

    return conn.commit()


def get_param(conn, user_id):
    return pandas.read_sql(f'''
    SELECT param_name
    FROM param 
    INNER JOIN user_param ON param.param_id = user_param.param_id
    WHERE users_id = {user_id}
    ''', conn)
