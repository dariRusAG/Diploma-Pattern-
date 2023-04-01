from app import app
from flask import render_template
from functions.role import *
from utils import get_db_connection
from models.scheme_model import *


@app.route('/scheme', methods=['GET', 'POST'])
def scheme():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    index_pattern = request.values.get('pattern')
    df_pattern = get_scheme_pattern(conn, int(index_pattern))

    return render_template(
        'scheme.html',

        # Пользователь
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,

        user_role=session['user_role'],
        auth_form=auth_form,
        reg_form=reg_form,

        # Выкройки
        pattern=df_pattern
    )
