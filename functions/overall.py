from flask import session
from models.favorites_model import *


def favorites_pattern(conn):
    if session['user_id'] is None:
        user_id = 0
    else:
        user_id = session['user_id']

    df_favorite_pattern = get_favorite_pattern(conn, user_id)

    favorite_list = []
    for i in range(len(df_favorite_pattern)):
        favorite_list.append(df_favorite_pattern.loc[i, "ID"])

    return df_favorite_pattern, favorite_list
