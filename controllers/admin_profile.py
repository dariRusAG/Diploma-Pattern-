from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.admin_profile_model import *


@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    conn = get_db_connection()

    admin_panel_button = None

    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    if request.values.get('add_category'):
        add_category(conn, request.values.get('new_category'))
        admin_panel_button = "Категории"

    elif request.values.get('delete_category'):
        category_id = int(request.values.get('delete_category'))
        admin_panel_button = "Категории"
        delete_category(conn, category_id)


    df_category = get_category(conn)
    print(df_category)
    html = render_template(
        'admin_profile.html',
        user_role=session['user_role'],
        admin_panel_button = admin_panel_button,
        category=df_category,
        len=len
    )

    return html
