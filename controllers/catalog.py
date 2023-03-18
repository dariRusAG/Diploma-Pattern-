from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.catalog_model import *
from forms import *


@app.route('/', methods=['GET', 'POST'])
def catalog():
    conn = get_db_connection()
    # нажата ли кнопка "войти"
    is_authorization = False
    # нажата ли кнопка "зарегистрироваться"
    is_registration = False
    # ошибка данных
    user_data_error = False
    # форма авторизации
    auth_form = AuthorizationForm(request.form)
    # форма регистрации
    reg_form = RegistrationForm(request.form)

    # нажата кнопка войти на странице каталога
    if request.values.get('authorization_button'):
        is_authorization = True

    # нажата кнопка регистрации
    elif request.values.get('registration_button'):
        is_registration = True

    # нажата кнопка авторизации после ввода данных
    elif request.values.get('authorization_user_button'):
        login = request.values.get('auth_login')
        password = request.values.get('auth_password')
        print(login)
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

    # нажата кнопка регистрации
    elif request.values.get('registration_user_button'):
        login = request.values.get('reg_login')
        password = request.values.get('reg_password')
        password_confirmation = request.values.get('password_confirm')
        if (get_user_id(conn, login) == "error") and (password == password_confirmation):
            registration(conn, login, password)
            session['user_id'] =f'{get_user_id(conn, login)}'
            session['user_role'] = "user"
        else:
            is_registration = True
            user_data_error = True

    # нажата кнопка выйти в личном кабинете
    elif request.values.get('exit_button'):
        session.pop('user_id', None)

    # если пользователь не вошел, то он гость
    if 'user_id' not in session:
        session['user_role'] = "guest"

    html = render_template(
        'catalog.html',
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,
        user_role=session['user_role'],
        auth_form=auth_form,
        reg_form=reg_form
    )

    return html
