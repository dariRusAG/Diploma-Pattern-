from flask import session, request
from models.catalog_favorites_model import *
from models.overall_model import *


def favorites_pattern(conn, category, complexity):
    if request.values.get('empty'):
        choice_favorite_pattern = request.values.get('pattern')
        if (choice_favorite_pattern != 0) or ('user_id' in session):
            add_pattern(conn, session['user_id'], choice_favorite_pattern)

    elif request.values.get('shaded'):
        choice_favorite_pattern = request.values.get('pattern')
        if (choice_favorite_pattern != 0) or ('user_id' in session):
            del_pattern(conn, choice_favorite_pattern)

    if 'user_id' not in session:
        user_id = 0
    else:
        user_id = session['user_id']

    df_favorite_pattern = get_favorite_pattern(conn, user_id, category, complexity)

    favorite_list = []
    for i in range(len(df_favorite_pattern)):
        favorite_list.append(df_favorite_pattern.loc[i, "ID"])

    return df_favorite_pattern, favorite_list
