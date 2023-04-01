from flask import request, session
from forms import *
from models.model_general import *


def role(conn):

    is_authorization = False  # нажата ли кнопка "войти"
    is_registration = False  # нажата ли кнопка "зарегистрироваться"
    user_data_error = ""  # ошибка данных

    auth_form = AuthorizationForm(request.form)  # форма авторизации
    reg_form = RegistrationForm(request.form)  # форма регистрации

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

        match is_correct_login_and_password(conn, login, password):

            case "user":
                session['user_id'] = f'{get_user_id(conn, login)}'
                session['user_role'] = "user"
            case "admin":
                session['user_id'] = f'{get_user_id(conn, login)}'
                session['user_role'] = "admin"
            case "error":
                is_authorization = True
                user_data_error = "Введен неправильный логин или пароль"

    # нажата кнопка регистрации
    elif request.values.get('registration_user_button'):
        login = request.values.get('reg_login')
        password = request.values.get('reg_password')
        password_confirmation = request.values.get('password_confirm')
        if get_user_id(conn, login) == "error":
            if password == password_confirmation:
                registration(conn, login, password)
                session['user_id'] = f'{get_user_id(conn, login)}'
                session['user_role'] = "user"
            else:
                is_registration = True
                user_data_error = "Пароли должны совпадать"
        else:
            is_registration = True
            user_data_error = "Пользователь с таким логином уже существует"

    # нажата кнопка выйти в личном кабинете
    elif request.values.get('exit_button'):
        session.pop('user_id', None)

    elif request.values.get('remove_profile_button'):
        to_delete_user(conn, session['user_id'])
        session.pop('user_id', None)

    # если пользователь не вошел, то он гость
    if 'user_id' not in session:
        session['user_role'] = "guest"

    return is_authorization, is_registration, user_data_error, auth_form, reg_form
