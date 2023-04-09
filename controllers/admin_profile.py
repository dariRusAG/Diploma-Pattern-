from app import app
from flask import render_template, request, session
from utils import get_db_connection
from functions.create_scheme import *

@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    conn = get_db_connection()
    # переменная для проверки нажатия кнопок
    checked_value = False
    # отвечает за то, какая вкладка на панели администратора открыта
    admin_panel_button = None

    create_user_scheme(conn)

    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    if request.values.get('add_category'):
        add_category(conn, request.values.get('new_category'))
        admin_panel_button = "Категории"

    elif request.values.get('delete_category'):
        category_id = int(request.values.get('delete_category'))
        admin_panel_button = "Категории"
        delete_category(conn, category_id)

    elif request.values.get('is_edit_category'):
        checked_value = True
        admin_panel_button = "Категории"

    elif request.values.get('edit_category'):
        category_id = int(request.values.get('edit_category'))
        category_name = request.values.get('edit_category_name')
        checked_value = False
        admin_panel_button = "Категории"
        update_category(conn, category_id, category_name)

    df_category = get_category(conn)
    html = render_template(
        'admin_profile.html',
        user_role=session['user_role'],
        admin_panel_button=admin_panel_button,
        category=df_category,
        checked_value=checked_value,
        len=len
    )

    return html
