from app import app
from flask import render_template
from functions.data_check import *
from utils import get_db_connection
from functions.create_scheme import *

def int_list(list_measures):
    temp = []
    [temp.append(x) for x in list_measures if (x not in temp) or (x in temp and x == 'ДИ')]
    return temp

@app.route('/scheme', methods=['GET', 'POST'])
def scheme():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    index_pattern = request.values.get('pattern')

    df_pattern = get_scheme_pattern(conn, int(index_pattern))
    df_measure = get_measure_detail(conn, int(index_pattern))

    measure_name_pattern = []
    measure_full_name_pattern = []
    details_lengths = []

    for index, row in df_measure.iterrows():
        for measure_name, measure_full_name in zip(row['Обозначение'].split(","), row['Полное_название'].split(",")):
            measure_name_pattern.append(measure_name)
            if measure_name != 'ДИ':
                measure_full_name_pattern.append(measure_full_name)
                details_lengths.append(row['Длина_детали'])
            if measure_name == 'ДИ':
                measure_full_name_pattern.append(measure_full_name + ' "' + row['Название_детали'] + '"')
                details_lengths.append(row['Длина_детали'])

    measure_name_pattern = int_list(measure_name_pattern)
    measure_full_name_pattern = int_list(measure_full_name_pattern)

    df_param = get_param_user(conn, session['user_id'])
    df_info_param = get_info_param(conn)

    param_value = []
    empty = 0
    checked_value = False

    name_scheme_pattern = ''
    name_scheme_detail = []

    gender_size = 'param_value_w'
    standard_size = 'base'

    # Если нажата одна из кнопок для заполнения стандартными мерками
    if request.values.get('fill_standard_param'):
        if request.values.get('page') == 'content-1':
            gender_size = request.values.get('gender_size-1')
        elif request.values.get('page') == 'content-2':
            gender_size = request.values.get('gender_size-2')

        if gender_size == 'param_value_w':
            df_param = get_param_standard_w(conn)
        elif gender_size == 'param_value_m':
            df_param = get_param_standard_m(conn)

        standard_size = request.values.get('fill_standard_param')
        for index, row in df_param.iterrows():
            all_size_param = row['Значение'].split(",")
            if standard_size == 'XS':
                row['Значение'] = float(all_size_param[0])
            if standard_size == 'S':
                row['Значение'] = float(all_size_param[1])
            if standard_size == 'M':
                row['Значение'] = float(all_size_param[2])
            if standard_size == 'L':
                row['Значение'] = float(all_size_param[3])
            if standard_size == 'XL':
                row['Значение'] = float(all_size_param[4])
            if standard_size == 'XXL':
                row['Значение'] = float(all_size_param[5])

    # Если нажата кнопка "Построить"
    if request.values.get('build_scheme-2'):
        id_detail = request.form.getlist('detail')
        int_id_detail = [int(x) for x in id_detail]
        param_value = request.form.getlist('param_value-2')
        param_designation = request.form.getlist('param_designation-2')
        df_param = pd.DataFrame(list(zip(int_id_detail, param_designation, param_value)),
                                columns=['ID', 'Обозначение', 'Значение'])

        for index, row in df_param.iterrows():
            if df_param.loc[index, 'Значение'] == '':
                empty = 1
                break

        if empty == 0:
            checked_value = True
            int_id_detail = list(set(int_id_detail))
            name_scheme_pattern = 'static/pdf/' + str(df_pattern.loc[0, "Название"]) + '.pdf'
            pdf = PdfPages(name_scheme_pattern)
            for id_detail in int_id_detail:
                df_param_detail = df_param.loc[(df_param['ID'] == id_detail)]
                create_user_scheme(conn, df_param_detail, id_detail, pdf)
                name_scheme_detail.append('static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg')
            pdf.close()

        standard_size = request.values.get('fill_standard_param')


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
        info_param=df_info_param,
        empty=empty,

        # Данные при построении выкройки целиком
        measure_name=measure_name_pattern,
        measure_full_name=measure_full_name_pattern,
        details_lengths=details_lengths,

        # Имена файлов
        name_scheme_pattern=name_scheme_pattern,
        name_scheme_detail=name_scheme_detail,

        # Размеры
        gender_size=gender_size,
        standard_size=standard_size,

        # Счетчики
        checked_value=checked_value,

        # Функции
        len=len,
        zip=zip
    )
