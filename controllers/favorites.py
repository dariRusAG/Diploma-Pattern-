from app import app
from flask import render_template
from utils import get_db_connection
from functions.role import *
from models.favorites_model import *


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    conn = get_db_connection()
    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    df_id_favorite_pattern = get_id_favorite_pattern(conn, 2)
    # df_favorite_pattern = get_favorite_pattern(conn, df_id_favorite_pattern)

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
        pattern=df_id_favorite_pattern,
        len=len
    )
