from app import app
from flask import render_template
from utils import get_db_connection
from functions.role import *
from functions.overall import *


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    df_favorite_pattern, favorite_list = favorites_pattern(conn)

    return render_template(
        'favorites.html',

        # Пользователь
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,

        user_role=session['user_role'],
        auth_form=auth_form,
        reg_form=reg_form,

        # Выкройки
        pattern=df_favorite_pattern,
        favorite_list=favorite_list,
        len=len
    )
