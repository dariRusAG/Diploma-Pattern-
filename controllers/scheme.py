from app import app
from flask import render_template
from functions.role import *
from utils import get_db_connection
from models.scheme_model import *


@app.route('/scheme', methods=['GET', 'POST'])
def scheme():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    index_pattern = request.values.get('pattern')
    df_pattern = get_scheme_pattern(conn, int(index_pattern))

    df_measure = get_measure_pattern(conn, int(index_pattern))
    df_param = get_param_user(conn, session['user_id'])

    param_value = []
    empty = 0

    # Если нажата кнопка "Построить"
    if request.values.get('build_scheme'):
        param_value = request.form.getlist('param_value')
        param_designation = request.form.getlist('param_designation')
        df_param = pd.DataFrame(list(zip(param_designation, param_value)), columns=['Обозначение', 'Значение'])

    for index, row in df_param.iterrows():
        if df_param.loc[index, 'Значение'] == '':
            empty = 1
            break

    return render_template(
        'scheme.html',

        # Пользователь
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,

        user_role=session['user_role'],
        auth_form=auth_form,
        reg_form=reg_form,

        # Выкройки
        pattern=df_pattern,
        measure=df_measure,
        param=df_param,
        param_value=param_value,
        empty=empty,

        # Функции
        len=len
    )
