from app import app
from flask import render_template
from functions.data_check import *
from utils import get_db_connection
from functions.create_scheme import *

def int_list(list_measures):
    temp = []
    [temp.append(x) for x in list_measures if (x not in temp) or (x in temp and x == 'ДИ')]
    return temp

def check_null_param(param):
    for index, row in param.iterrows():
        if param.loc[index, 'Значение'] == '':
            return 1
    return 0

@app.route('/scheme', methods=['GET', 'POST'])
def scheme():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error, auth_form, reg_form = role(conn)

    index_pattern = request.values.get('pattern')
    page = request.values.get('page')

    if index_pattern is not None and page is not None:
        session['pattern'] = index_pattern
        session['page'] = page
    else:
        index_pattern = session['pattern']
        page = session['page']

    df_pattern = get_scheme_pattern(conn, int(index_pattern))
    df_measure = get_measure_pattern(conn, int(index_pattern))

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
        if page == '#content-1':
            gender_size = request.values.get('gender_size-1')
        elif page == '#content-2':
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

    # Если нажата кнопка "Построить" в разделе построения по деталям
    if request.values.get('build_scheme'):
        if page == '#content-1':
            param_value = request.form.getlist('param_value')
            param_designation = request.form.getlist('param_designation')

            name_scheme_pattern = 'static/pdf/' + str(df_pattern.loc[0, "Название"]) + '.pdf'
            pdf = PdfPages(name_scheme_pattern)
            df_param = pd.DataFrame(columns=['ID', 'Обозначение', 'Значение'])

            list_id_detail = df_measure['ID'].tolist()
            for id_detail in list_id_detail:
                df_measure_detail = get_measure_detail(conn, id_detail)
                param_value_all = []
                for index, row in df_measure_detail.iterrows():
                    index_param_designation = param_designation.index(row['Обозначение'])
                    param_value_all.append(param_value[index_param_designation])
                    if row['Обозначение'] == 'ДИ':
                        param_value.remove(param_value[index_param_designation])
                        param_designation.remove(param_designation[index_param_designation])

                df_param_detail = pd.DataFrame(list(zip(
                    df_measure_detail['ID'].tolist(),
                    df_measure_detail['Обозначение'].tolist(),
                    df_measure_detail['Полное_название'].tolist(),
                    param_value_all)),
                    columns=['ID', 'Обозначение', 'Полное_название', 'Значение'])

                df_param = pd.concat([df_param, df_param_detail], axis=0, ignore_index=True)

                if check_null_param(df_param) == 0:
                    checked_value = True
                    create_user_scheme(conn, df_param_detail, id_detail, pdf)
                    name_scheme_detail.append(
                        'static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg')

            for index, row in df_param.iterrows():
                if row['Обозначение'] == 'ДИ':
                    new_measure_full_name = row['Полное_название'] + ' "' + str(get_detail_name(conn, row['ID'])) + '"'
                    row['Полное_название'] = new_measure_full_name

            df_param = df_param.drop_duplicates(subset=['Полное_название', 'Значение'], ignore_index=True)

            pdf.close()
            # standard_size = request.values.get('fill_standard_param')

        elif page == '#content-2':
            list_id_detail = request.form.getlist('detail')
            param_value = request.form.getlist('param_value')
            param_designation = request.form.getlist('param_designation')
            df_param = pd.DataFrame(list(zip(list_id_detail, param_designation, param_value)),
                                    columns=['ID', 'Обозначение', 'Значение'])

            if check_null_param(df_param) == 0:
                checked_value = True
                name_scheme_pattern = 'static/pdf/' + str(df_pattern.loc[0, "Название"]) + '.pdf'
                pdf = PdfPages(name_scheme_pattern)
                list_id_detail = list(set(list_id_detail))
                for id_detail in list_id_detail:
                    df_param_detail = df_param.loc[(df_param['ID'] == id_detail)]
                    create_user_scheme(conn, df_param_detail, id_detail, pdf)
                    name_scheme_detail.append(
                        'static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg')
                pdf.close()

            # standard_size = request.values.get('fill_standard_param')

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
        page=page,

        # Размеры
        gender_size=gender_size,
        standard_size=standard_size,

        # Счетчики
        checked_value=checked_value,

        # Функции
        len=len,
        zip=zip,
        str=str
    )
