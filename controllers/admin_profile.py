from app import app
from flask import render_template, request, session
from models.admin_profile_model import *
from utils import get_db_connection


@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    conn = get_db_connection()
    # переменная для проверки нажатия кнопок
    checked_value = ['False', '']
    # отвечает за то, какая вкладка на панели администратора открыта
    admin_panel_button = None

    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    if request.values.get('add_category'):
        if get_category_id(conn, request.values.get('new_category')) == "error" and request.values.get('new_category') != '':
            add_category(conn, request.values.get('new_category'))
        admin_panel_button = "Категории"

    elif request.values.get('delete_category'):
        category_id = int(request.values.get('delete_category'))
        admin_panel_button = "Категории"
        delete_category(conn, category_id)

    elif request.values.get('is_edit_category'):
        checked_value[0] = True
        checked_value[1] = int(request.values.get('is_edit_category_id'))
        admin_panel_button = "Категории"

    elif request.values.get('edit_category'):
        category_id = int(request.values.get('edit_category'))
        if get_category_id(conn, request.values.get('edit_category_name')) == "error" and request.values.get('edit_category_name') != '':
            category_name = request.values.get('edit_category_name')
            update_category(conn, category_id, category_name)
        checked_value = False
        admin_panel_button = "Категории"

    elif request.values.get('add_formula'):
        if get_formula_id(conn, request.values.get('new_formula_name'), request.values.get('new_formula_value')) == "error" \
            and request.values.get('new_formula_name') != '' and request.values.get('new_formula_value') != '':
            add_formula(conn, request.values.get('new_formula_name'), request.values.get('new_formula_value'))
        admin_panel_button = "Формулы"

    df_category = get_category(conn)
    df_formula = get_formula(conn)
    df_measure = get_measure(conn)
    df_line = get_line(conn)
    html = render_template(
        'admin_profile.html',
        user_role=session['user_role'],
        admin_panel_button=admin_panel_button,
        category_list=df_category,
        checked_value=checked_value,
        formula_list=df_formula,
        measure_list=df_measure,
        line_list=df_line,
        len=len
    )

    return html
