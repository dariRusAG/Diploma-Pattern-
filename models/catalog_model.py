import pandas as pd

def is_correct_login_and_password(conn,login,password):
    try:
        return pd.read_sql('''SELECT role
        FROM user
        WHERE login = :login AND password = :password;
        ''', conn,params={"login":login, "password":password}).values[0][0]
    except IndexError:
        return "error"

def get_user_id(conn,login):
    return pd.read_sql('''SELECT user_id FROM user WHERE login = :login
    ''', conn,params={"login":login}).values[0][0]