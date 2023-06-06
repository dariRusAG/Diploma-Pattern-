import math

from flask import request, session
from functions.create_scheme import create_user_scheme
from models.admin_profile_model import *
from models.model_general import *
from models.scheme_model import get_param_standard_w
from models.user_profile_model import is_correct_user_data


def role(conn):

    is_authorization = False  # нажата ли кнопка "войти"
    is_registration = False  # нажата ли кнопка "зарегистрироваться"
    user_data_error = ""  # ошибка данных

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
        if login == '' or password == '' or password_confirmation == '':
            is_registration = True
            user_data_error = "Введены пустые данные"
        elif len(login) < 4:
            is_registration = True
            user_data_error = "Логин должен быть больше 4 символов"
        elif len(login) > 15:
            is_registration = True
            user_data_error = "Логин должен быть меньше 15 символов"
        elif len(password) < 8:
            is_registration = True
            user_data_error = "Пароль должен быть больше 8 символов"
        elif len(password) > 60:
            is_registration = True
            user_data_error = "Пароль должен быть меньше 60 символов"
        elif get_user_id(conn, login) != "error":
            is_registration = True
            user_data_error = "Пользователь с таким логином уже существует"
        elif password != password_confirmation:
                is_registration = True
                user_data_error = "Пароли должны совпадать"
        else:
            registration(conn, login, password)
            session['user_id'] = f'{get_user_id(conn, login)}'
            new_user_params(conn, session['user_id'])
            session['user_role'] = "user"

    # нажата кнопка выйти в личном кабинете
    elif request.values.get('exit_button'):
        session.pop('user_id', None)
        session.pop('page', None)

    elif request.values.get('remove_profile_button'):
        to_delete_user(conn, session['user_id'])
        session.pop('user_id', None)
        session.pop('page', None)

    # если пользователь не вошел, то он гость
    if 'user_id' not in session:
        session['user_role'] = "guest"

    return is_authorization, is_registration, user_data_error


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_correct_overall(name):
    if name == '':
        return "Ошибка! Введено пустое поле"
    elif not name.replace(" ", "").isalpha():
        return "Ошибка! В названии не должно быть цифр или символов"
    else:
        return 'True'


def is_correct_category(conn, name, category_id):
    if is_correct_overall(name) != 'True':
        return is_correct_overall(name)
    elif get_category_id(conn, name) != "error" and get_category_id(conn, name) != category_id:
        return "Ошибка! Такая категория уже существует"
    else:
        return 'True'


def is_correct_formula(conn, name, value, formula_id):
    df_param = get_param_standard_w(conn)
    for index, row in df_param.iterrows():
        all_size_param = row['Значение'].split(",")
        row['Значение'] = float(all_size_param[2])
    df_param_detail = dict(zip(df_param["Обозначение"], df_param["Значение"]))
    df_param_detail['Корень'] = math.sqrt
    df_param_detail['Степень'] = math.pow
    df_param_detail['ДИ'] = 10
    if value == '':
        return "Ошибка! Введено пустое поле"
    else:
        try:
            eval(value, df_param_detail)
        except Exception:
            return "Ошибка! Неверный синтаксис формулы"

        if is_correct_overall(name.replace("_"," ")) != 'True':
            return is_correct_overall(name)
        elif get_formula_id(conn, name) != "error" and get_formula_id(conn, name) != formula_id:
            return "Ошибка! Такое название формулы уже существует"
        elif value == '':
            return "Ошибка! Введено пустое поле"
        elif get_formula_id_by_value(conn, value) != "error" and get_formula_id_by_value(conn, value) != formula_id:
            return "Ошибка! Такая формула уже существует"
        else:
            return 'True'


def is_correct_detail(conn, name, size, detail_id):
    if detail_id == '':
        detail_id = -1
    if is_correct_overall(name) != 'True':
        return is_correct_overall(name)
    elif get_detail_id(conn, name) != "error" and get_detail_id(conn, name) != int(detail_id):
        return "Ошибка! Такое название детали уже существует"
    elif is_float(size) != True and size != '':
        return "Ошибка! Неверное значение эталонной длины"
    else:
        return 'True'


def is_correct_pattern(conn, name, category, picture, detail_list, pattern_id):
    if is_correct_overall((name.replace(" ", "")).replace("-", "")) != 'True':
        return is_correct_overall(name)
    elif get_pattern_id(conn, name) != "error" and get_pattern_id(conn, name) != pattern_id:
        return "Ошибка! Выкройка с таким именем уже существует"
    elif picture == '':
        return "Ошибка! Вместо картинки введено пустое поле"
    elif not detail_list:
        return "Ошибка! Отсутствуют детали"
    elif category is None:
        return "Ошибка! Отсутствует категория"
    else:
        return 'True'


def is_correct_scheme(conn, df_param_detail, detail_id, pdf):
    scheme = create_user_scheme(conn, df_param_detail, detail_id, pdf, "admin")
    if scheme == "error_mes":
        return "Ошибка! Выбраны не все мерки для формул"
    elif scheme == "error_form":
        return "Ошибка! Выбраны не все формулы для линий"
    elif scheme == "error_line":
        return "Ошибка! Недопустимые значения линий"
    else:
        return 'True'


def is_correct_login_password(conn, login, password, user_id):

    if login == '':
        return "Ошибка! Логин не может быть пустым"
    elif password == '':
        return "Ошибка! Пароль не может быть пустым"
    elif len(login) < 4:
        return "Логин должен быть больше 4 символов"
    elif len(login) > 15:
        return "Логин должен быть меньше 15 символов"
    elif len(password) < 8:
        return "Пароль должен быть больше 8 символов"
    elif len(password) > 60:
        return "Пароль должен быть меньше 60 символов"
    elif is_correct_user_data(conn, login, user_id) != "error":
        return "Ошибка! Такой логин уже занят"
    else:
        return "True"


def is_correct_params(conn, elem, name):
    min = get_params_max_min(conn, name)[0]
    max = get_params_max_min(conn, name)[1]
    if str(elem) == '':
        return "True"
    if not is_float(elem):
        return "Ошибка! Значение параметра " + str(name) + " должно быть числом"
    elif min > float(elem) or max < float(elem):
        return "Ошибка! Значение параметра " + str(name) + " должно быть от " + str(min) + " до " + str(max)
    else:
        return "True"

def is_correct_params_scheme(conn, elem, name, detail_name, func):
    min = get_params_max_min(conn, name)[0]
    max = get_params_max_min(conn, name)[1]
    if func == "detail_pattern" or str(name) == "ДИ":
        if elem == '':
            return "Ошибка! Значение " + str(name) +" у детали " + '"' + detail_name + '"' + " не должно быть пустым"
        elif not is_float(elem):
            return "Ошибка! Значение параметра " + str(name)  + " у детали " + '"' + detail_name + '"' +  " должно быть числом"
        elif min > float(elem) or max < float(elem):
            return "Ошибка! Значение параметра " + str(name)  + " у детали " + '"' + detail_name + '"' + " должно быть от " + str(min) + " до " + str(max)
        else:
            return "True"
    else:
        if elem == '':
            return "Ошибка! Значение " + str(name) + " не должно быть пустым"
        elif not is_float(elem):
            return "Ошибка! Значение параметра " + str(name) + " должно быть числом"
        elif min > float(elem) or max < float(elem):
            return "Ошибка! Значение параметра " + str(name) + " должно быть от " + str(min) + " до " + str(max)
        else:
            return "True"