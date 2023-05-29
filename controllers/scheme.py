from app import app
from flask import render_template
from functions.data_check import *
from utils import get_db_connection
from functions.create_scheme import *
from models.scheme_model import *
from matplotlib.backends.backend_pdf import PdfPages


def int_list(list_measures):
    temp = []
    [temp.append(x) for x in list_measures if (x not in temp) or (x in temp and x == 'ДИ')]
    return temp

def init_measure(df_measure):
    measure_name_pattern = []
    measure_full_name_pattern = []
    details_lengths = []

    for index, row in df_measure.iterrows():
        for measure_name, measure_full_name in zip(row['Обозначение'].split(","),
                                                   row['Полное_название'].split(",")):
            measure_name_pattern.append(measure_name)
            if measure_name != 'ДИ':
                measure_full_name_pattern.append(measure_full_name)
            if measure_name == 'ДИ':
                measure_full_name_pattern.append('Длина детали "' + row['Название_детали'] + '"')

    measure_name_pattern = int_list(measure_name_pattern)
    measure_full_name_pattern = int_list(measure_full_name_pattern)

    check_measure = []

    for index, row in df_measure.iterrows():
        for measure_name in row['Обозначение'].split(","):
            if measure_name not in check_measure or measure_name == 'ДИ':
                details_lengths.append(row['Длина_детали'])
                check_measure.append(measure_name)

    return measure_name_pattern, measure_full_name_pattern, details_lengths

# Автозаполнение для вкладок построения
def autocomplete(gender_size_html, df_param, conn):
    gender_size = request.values.get(str(gender_size_html))
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

    return gender_size, standard_size, df_param

def check_error_param(df_param, id_detail, error_info, type_pattern, conn):
    for i in range(len(df_param)):
        if df_param.loc[i, "Обозначение"] != '':
            error = is_correct_params_scheme(conn,
                                             df_param.loc[i, "Значение"],
                                             df_param.loc[i, "Обозначение"],
                                             str(get_detail_name(conn, id_detail[i])),
                                             type_pattern)

            if error != "True" and error_info[0].count(error) == 0:
                error_info[0].append(error)

    return error_info

# Общая начальная обработка перед построением схемы выкройки
def init_build_scheme(index_pattern, list_id_detail, conn):
    param_value = request.form.getlist('param_value')
    param_designation = request.form.getlist('param_designation')

    list_id_detail_int = [int(x) for x in list_id_detail]

    df_param_detail_no_measure = get_detail_no_measure(conn, index_pattern, list_id_detail_int)
    for index, row in df_param_detail_no_measure.iterrows():
        row['ID'] = str(row['ID'])

    list_id_detail += df_param_detail_no_measure['ID'].tolist()

    return param_value, param_designation, list_id_detail, df_param_detail_no_measure


@app.route('/scheme', methods=['GET', 'POST'])
def scheme():
    conn = get_db_connection()

    is_authorization, is_registration, user_data_error = role(conn)

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

    measure_name_pattern, measure_full_name_pattern, details_lengths = init_measure(df_measure)

    df_info_param = get_info_param(conn)

    gender_size_1 = 'param_value_w'
    standard_size_1 = 'base'

    gender_size_2 = 'param_value_w'
    standard_size_2 = 'base'

    if 'user_id' in session:
        df_param_1 = get_param_user(conn, session['user_id'])
        df_param_2 = get_param_user(conn, session['user_id'])
    else:
        df_param_1 = pd.DataFrame(columns=['ID', 'Обозначение', 'Значение'])
        df_param_2 = pd.DataFrame(columns=['ID', 'Обозначение', 'Значение'])

    param_value = []

    checked_value_1 = False
    checked_value_2 = False

    name_scheme_pattern = ''
    name_scheme_detail_1 = []
    name_scheme_detail_2 = []

    list_size = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

    error_info = [[], [], [], []]

    # Если открыта вкладка построения по общим меркам
    if page == '#content-1':

        if request.values.get('fill_standard_param'):
            gender_size_1, standard_size_1, df_param_1 = autocomplete('gender_size-1', df_param_1, conn)

        if request.values.get('build_scheme'):
            param_value, param_designation, list_id_detail, df_param_detail_no_measure = init_build_scheme(index_pattern, df_measure['ID'].tolist(), conn)

            df_param_1 = pd.DataFrame(columns=['ID', 'Обозначение', 'Полное_название', 'Значение'])

            name_scheme_pattern = 'static/pdf/' + str(df_pattern.loc[0, "Название"]) + '.pdf'
            pdf = PdfPages(name_scheme_pattern)

            # Обработка мерок и параметров для построения по деталям
            for id_detail in list_id_detail:
                df_measure_detail = get_measure_detail(conn, id_detail)

                param_value_all = []
                for index, row in df_measure_detail.iterrows():
                    index_param_designation = param_designation.index(row['Обозначение'])
                    param_value_all.append(param_value[index_param_designation])
                    if row['Обозначение'] == 'ДИ':
                       param_designation[index_param_designation] = ''

                df_param_detail = pd.DataFrame(list(zip(
                    df_measure_detail['ID'].tolist(),
                    df_measure_detail['Обозначение'].tolist(),
                    df_measure_detail['Полное_название'].tolist(),
                    param_value_all)),
                    columns=['ID', 'Обозначение', 'Полное_название', 'Значение'])

                df_param_1 = pd.concat([df_param_1, df_param_detail], axis=0, ignore_index=True)

                # Проверка на ошибки
                for i in range(len(df_param_1)):
                    if df_param_1.loc[i, "Обозначение"] != '':
                        error = is_correct_params_scheme(conn, df_param_1.loc[i, "Значение"],
                                                         df_param_1.loc[i, "Обозначение"],
                                                         str(get_detail_name(conn, id_detail)), "all_pattern")
                        if error != "True" and error_info[0].count(error) == 0:
                            error_info[0].append(error)
                            if df_param_1.loc[i, "Обозначение"] == "ДИ":
                                error_info[2].append('Длина детали "' + str(get_detail_name(conn, id_detail)) + '"')
                            else:
                                error_info[2].append(df_param_1.loc[i, "Полное_название"])

                if len(error_info[0]) == 0:
                    checked_value_1 = True
                    create_user_scheme(conn, df_param_detail, id_detail, pdf, "user")
                    name_scheme_detail_1.append(
                        'static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg')

            for index, row in df_param_1.iterrows():
                if row['Обозначение'] == 'ДИ':
                    new_measure_full_name = 'Длина детали "' + str(get_detail_name(conn, row['ID'])) + '"'
                    row['Полное_название'] = new_measure_full_name

            df_param_1 = df_param_1.drop_duplicates(subset=['Полное_название', 'Обозначение'], ignore_index=True)

            pdf.close()
            standard_size_1 = request.values.get('fill_standard_param')

    # Если открыта вкладка построения по раздельным меркам
    elif page == '#content-2':

        if request.values.get('fill_standard_param'):
            gender_size_2, standard_size_2, df_param_2 = autocomplete('gender_size-2', df_param_2, conn)

        if request.values.get('build_scheme'):
            param_value, param_designation, list_id_detail, df_param_detail_no_measure = init_build_scheme(index_pattern, request.form.getlist('detail'), conn)

            df_param_2 = pd.DataFrame(list(zip(list_id_detail, param_designation, param_value)),
                                      columns=['ID', 'Обозначение', 'Значение'])

            df_param_2 = pd.concat([df_param_2, df_param_detail_no_measure], axis=0, ignore_index=True)

            # Проверка на ошибки
            for i in range(len(df_param_2)):
                if df_param_2.loc[i, "Обозначение"] != '':
                    error = is_correct_params_scheme(conn, df_param_2.loc[i, "Значение"],
                                                     df_param_2.loc[i, "Обозначение"],
                                                     str(get_detail_name(conn, list_id_detail[i])), "detail_pattern")
                    if error != "True" and error_info[1].count(error) == 0:
                        error_info[1].append(error)
                        error_info[3].append('error')
                    else:
                        error_info[3].append('')

            if len(error_info[1]) == 0:
                checked_value_2 = True
                name_scheme_pattern = 'static/pdf/' + str(df_pattern.loc[0, "Название"]) + '.pdf'
                pdf = PdfPages(name_scheme_pattern)

                list_id_detail = list(set(list_id_detail))

                for id_detail in list_id_detail:
                    df_param_detail = df_param_2.loc[(df_param_2['ID'] == id_detail)]
                    create_user_scheme(conn, df_param_detail, id_detail, pdf, "user")
                    name_scheme_detail_2.append(
                        'static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg')
                pdf.close()

            standard_size_2 = request.values.get('fill_standard_param')

    return render_template(
        'scheme.html',

        # Пользователь
        is_authorization=is_authorization,
        is_registration=is_registration,
        user_data_error=user_data_error,
        user_role=session['user_role'],

        # Выкройки
        pattern=df_pattern,
        measure=df_measure,
        param_1=df_param_1,
        param_2=df_param_2,
        param_value=param_value,
        info_param=df_info_param,
        error_info=error_info,

        # Данные при построении выкройки целиком
        measure_name=measure_name_pattern,
        measure_full_name=measure_full_name_pattern,
        details_lengths=details_lengths,

        # Имена файлов
        name_scheme_pattern=name_scheme_pattern,
        name_scheme_detail_1=name_scheme_detail_1,
        name_scheme_detail_2=name_scheme_detail_2,
        page=page,

        # Размеры
        list_size=list_size,
        gender_size_1=gender_size_1,
        standard_size_1=standard_size_1,
        gender_size_2=gender_size_2,
        standard_size_2=standard_size_2,

        # Счетчики
        checked_value_1=checked_value_1,
        checked_value_2=checked_value_2,

        # Функции
        len=len,
        zip=zip,
        str=str
    )
