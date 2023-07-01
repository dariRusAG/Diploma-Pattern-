from app import app
from flask import render_template
from functions.data_check import *
from utils import get_db_connection
from models.catalog_favorites_model import *


def favorites_pattern(conn, category, complexity, is_authorization):

    if 'user_id' not in session:
        user_id = 0
    else:
        user_id = session['user_id']

    if request.values.get('shaded'):
        if user_id == 0:
            is_authorization = True
        choice_favorite_pattern = request.values.get('pattern')
        if (choice_favorite_pattern != 0) and ('user_id' in session):
            add_pattern(conn, session['user_id'], choice_favorite_pattern)

    elif request.values.get('empty'):
        choice_favorite_pattern = request.values.get('pattern')
        if (choice_favorite_pattern != 0) and ('user_id' in session):
            del_pattern(conn, choice_favorite_pattern)

    df_favorite_pattern = get_favorite_pattern(conn, user_id, category, complexity)

    favorite_list = []
    for i in range(len(df_favorite_pattern)):
        favorite_list.append(df_favorite_pattern.loc[i, "ID"])

    return df_favorite_pattern, favorite_list, is_authorization


@app.route('/', methods=['GET', 'POST'])
def catalog_favorites():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error = role(conn)

    new_complexity = 0

    df_pattern = []
    df_favorite_pattern = []
    favorite_list = []

    #
    # if 'complexity' in session:
    #     complexity = int(session['complexity'])
    # else:
    #     complexity = 0

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
        session['category'] = category
        complexity = int(request.values.get('complexity_shaded'))
        session['complexity'] = complexity

        df_favorite_pattern, favorite_list, is_authorization = favorites_pattern(conn, category, complexity, is_authorization)
        df_pattern = get_pattern(conn, category, complexity)

    # Если нажата кнопка выбора сложности
    elif request.values.get('complexity'):
        if 'category' in session:
            old_category = session['category']
        else:
            old_category = []

        complexity = int(request.values.get('complexity_shaded'))
        new_complexity = int(request.values.get('complexity'))

        df_favorite_pattern, favorite_list, is_authorization = favorites_pattern(conn, old_category, complexity, is_authorization)
        df_pattern = get_pattern(conn, old_category, complexity)

        category = request.form.getlist('category')

    elif request.values.get('shaded') or request.values.get('empty'):
        if 'category' in session:
            category = session['category']
        else:
            category = []

        if 'complexity' in session:
            complexity = int(session['complexity'])
        else:
            complexity = 0

        df_favorite_pattern, favorite_list, is_authorization = favorites_pattern(conn, category, complexity, is_authorization)
        df_pattern = get_pattern(conn, category, complexity)

    # Если нажата кнопка "Очистить"
    else:
        category = []
        complexity = 0
        session.pop('category', None)
        session.pop('complexity', None)

    if len(df_pattern) == 0 and complexity == 0:
        df_favorite_pattern, favorite_list, is_authorization = favorites_pattern(conn, [], 0, is_authorization)
        df_pattern = get_pattern(conn, [], 0)

    df_category = get_category(conn)

    if 'page' in session:
        if session['page'] == "favorites":
            df_pattern = df_favorite_pattern
    else:
        session['page'] = "catalog"
        session['title'] = "Каталог"

    if session['user_role'] != "admin":
        return render_template(
            'catalog_favorites.html',
            title=session['title'],
            page=session['page'],

            # Пользователь
            is_authorization=is_authorization,
            is_registration=is_registration,
            user_data_error=user_data_error,

            user_role=session['user_role'],

            # Выбор фильтров
            category=df_category,
            choice_category=category,
            choice_complexity=complexity,
            new_complexity=new_complexity,

            # Выкройки
            pattern=df_pattern,
            favorite_list=favorite_list,

            # Функции
            len=len,
            str=str,
            reversed=reversed
        )

    else:
        return render_template(
            'admin_profile.html',
            user_role=session['user_role'])