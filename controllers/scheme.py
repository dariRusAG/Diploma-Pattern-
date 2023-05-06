from app import app
from flask import render_template
from functions.role import *
from utils import get_db_connection
from functions.create_scheme import *


@app.route('/scheme', methods=['GET', 'POST'])
def scheme():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    index_pattern = request.values.get('pattern')
    df_pattern = get_scheme_pattern(conn, int(index_pattern))

    df_measure = get_measure_detail(conn, int(index_pattern))
    df_param = get_param_user(conn, session['user_id'])

    param_value = []
    empty = 0
    checked_value = False
    name_scheme = []

    x_deviation, y_deviation = [], []

    # Если нажата кнопка "Построить"
    if request.values.get('build_scheme'):
        id_detail = request.form.getlist('detail')
        int_id_detail = [int(x) for x in id_detail]
        param_value = request.form.getlist('param_value')
        param_designation = request.form.getlist('param_designation')
        df_param = pd.DataFrame(list(zip(int_id_detail, param_designation, param_value)),
                                columns=['ID', 'Обозначение', 'Значение'])

        for index, row in df_param.iterrows():
            if df_param.loc[index, 'Значение'] == '':
                empty = 1
                break

        if empty == 0:
            checked_value = True
            int_id_detail = list(set(int_id_detail))
            for id_detail in int_id_detail:
                df_param_detail = df_param.loc[(df_param['ID'] == id_detail)]
                create_user_scheme(conn, df_param_detail, id_detail)
                name_scheme.append('static/' + str(id_detail) + '.jpg')

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
        name_scheme=name_scheme,

        # Счетчики
        checked_value=checked_value,

        # Функции
        len=len,
        zip=zip
    )
