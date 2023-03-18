from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.catalog_model import *


@app.route('/', methods=['GET', 'POST'])
def catalog():
    conn = get_db_connection()
    # нажата ли кнопка "войти"
    is_authorization = False
    # нажата ли кнопка "зарегистрироваться"
    is_registration = False
    # ошибка данных
    user_data_error = False

    # нажата кнопка войти на странице каталога
    if request.values.get('authorization_button'):
        is_authorization = True

    # нажата кнопка регистрации
    elif request.values.get('registration_button'):
        is_registration = True

    # нажата кнопка авторизации после ввода данных
    elif request.values.get('authorization_user_button'):
        login = request.values.get('login')
        password = request.values.get('password')
        match is_correct_login_and_password(conn, login,password):
            case "user":
                session['user_id'] =f'{get_user_id(conn, login)}'
                session['user_role'] = "user"
            case "admin":
                session['user_id'] =f'{get_user_id(conn, login)}'
                session['user_role'] = "admin"
            case "error":
                is_authorization = True
                user_data_error = True

    if 'user_id' in session:
        user_session = True
    else:
        user_session = False

    html = render_template(
        'catalog.html',
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,
        user_session=user_session
    )

    return html
