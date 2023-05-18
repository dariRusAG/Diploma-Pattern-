from app import app
from flask import render_template
from functions.data_check import *
from utils import get_db_connection
from models.catalog_favorites_model import *


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


@app.route('/', methods=['GET', 'POST'])
def catalog_favorites():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    # Если нажата кнопка "Список избранного"
    if request.values.get('favorites'):
        session['title'] = "Список избранного"
        session['page'] = "favorites"

    # Если нажата кнопка "Каталог"
    elif request.values.get('catalog'):
        session['title'] = "Каталог"
        session['page'] = "catalog"

    # Если нажата кнопка "Найти"
    if request.values.get('search'):
        category = request.form.getlist('category')
        complexity = request.form.getlist('complexity')

    # Если нажата кнопка "Очистить"
    else:
        category = []
        complexity = []

    df_favorite_pattern, favorite_list = favorites_pattern(conn, category, complexity)
    df_category = get_category(conn)
    df_pattern = get_pattern(conn, category, complexity)

    if 'page' in session:
        if session['page'] == "favorites":
            df_pattern = df_favorite_pattern
    else:
        session['page'] = "catalog"
        session['title'] = "Каталог"
        category = []
        complexity = []

    return render_template(
        'catalog_favorites.html',
        title=session['title'],
        page=session['page'],

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

        # Выкройки
        pattern=df_pattern,
        favorite_list=favorite_list,

        # Функции
        len=len,
        str=str
    )
