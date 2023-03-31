from app import app
from flask import render_template
from functions.role import *
from utils import get_db_connection
from functions.overall import *


@app.route('/', methods=['GET', 'POST'])
def catalog():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)
    df_favorite_pattern, favorite_list = favorites_pattern(conn)

    df_category = get_category(conn)

    # Если нажата кнопка "Найти"
    if request.values.get('search'):
        category = request.form.getlist('category')
        complexity = request.form.getlist('complexity')

    # Если нажата кнопка "Очистить" или вход на сайт впервые
    else:
        category = []
        complexity = []

    df_pattern = get_pattern(conn, category, complexity)

    return render_template(
        'catalog.html',

        # Пользователь
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,

        user_role=session['user_role'],
        auth_form=auth_form,
        reg_form=reg_form,

        # Выбор фильтров
        category=df_category,
        choice_category=category,
        choice_complexity=complexity,
        len=len,
        str=str,

        # Выкройки
        pattern=df_pattern,
        favorite_list=favorite_list
    )
