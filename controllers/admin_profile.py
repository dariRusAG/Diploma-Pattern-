from app import app
from flask import render_template, request, session

from functions.data_check import *
from models.admin_profile_model import *
from models.model_general import get_detail_name
from utils import get_db_connection
from functions.create_scheme import *
import os


# Подсчет сложности выкройки
def difficulty_calculation(category, number_details, number_measurements):
    complexity = number_details * number_measurements * 0.5

    if category == 'Юбки':
        complexity *= 1
    elif category == 'Футболки' or category == 'Брюки':
        complexity *= 2
    elif category == 'Рубашки':
        complexity *= 3
    elif category == 'Платья':
        complexity *= 4

    if complexity in range(1, 20):
        complexity = 1
    elif complexity in range(21, 40):
        complexity = 2
    elif complexity in range(41, 60):
        complexity = 3
    elif complexity in range(61, 80):
        complexity = 4
    elif complexity in range(81, 100):
        complexity = 5

    return complexity


@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    conn = get_db_connection()
    # переменная для проверки нажатия кнопок
    checked_value = ['False', '']
    # отвечает за то, какая вкладка на панели администратора открыта
    admin_panel_button = None
    session.modified = True
    name_scheme = ''
    info_about_some = ['', '']
    error_info = ''

    if 'detail' not in session:
        session['detail'] = []
    if 'detail_lines' not in session:
        session['detail_lines'] = []
    if 'edit_detail_info' not in session:
        session['edit_detail_info'] = ['']

    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    if request.values.get('add_category'):
        if is_correct_category(conn, request.values.get('new_category')) == 'True':
            add_category(conn, str(request.values.get('new_category')).strip())
        else:
            error_info = is_correct_category(conn, request.values.get('new_category'))
        admin_panel_button = "Категории"

    elif request.values.get('delete_category'):
        category_id = int(request.values.get('delete_category'))
        admin_panel_button = "Категории"
        delete_category(conn, category_id)

    elif request.values.get('is_edit_category'):
        checked_value[0] = True
        checked_value[1] = int(request.values.get('is_edit_category_id'))
        admin_panel_button = "Категории"

    elif request.values.get('edit_category'):
        category_id = int(request.values.get('edit_category'))
        if is_correct_category(conn, request.values.get('edit_category_name')) == 'True':
            category_name = request.values.get('edit_category_name')
            update_category(conn, category_id, category_name)
        else:
            error_info = is_correct_category(conn, request.values.get('edit_category_name'))
        checked_value = False
        admin_panel_button = "Категории"

    elif request.values.get('add_formula'):
        if is_correct_formula(conn, request.values.get('new_formula_name'),
                              request.values.get('new_formula_value')) == 'True':
            add_formula(conn, str(request.values.get('new_formula_name')).strip(),
                        str(request.values.get('new_formula_value')).strip())
        else:
            error_info = is_correct_formula(conn, request.values.get('new_formula_name'),
                                            request.values.get('new_formula_value'))
        admin_panel_button = "Формулы"

    elif request.values.get('delete_formula'):
        formula_id = int(request.values.get('delete_formula'))
        admin_panel_button = "Формулы"
        delete_formula(conn, formula_id)

    elif request.values.get('is_edit_formula'):
        checked_value[0] = True
        checked_value[1] = int(request.values.get('is_edit_formula_id'))
        admin_panel_button = "Формулы"

    elif request.values.get('edit_formula'):
        formula_id = int(request.values.get('edit_formula'))
        formula_name = str(request.values.get('edit_formula_name')).strip()
        formula_value = str(request.values.get('edit_formula_value')).strip()
        if is_correct_edit_formula(conn, request.values.get('edit_formula_name'),
                                   request.values.get('edit_formula_value')) == 'True':
            update_formula(conn, formula_id, formula_name, formula_value)
        else:
            error_info = is_correct_edit_formula(conn, request.values.get('edit_formula_name'),
                                                 request.values.get('edit_formula_value'))
        checked_value = False
        admin_panel_button = "Формулы"

    elif admin_panel_button == "Добавить Линии" or request.values.get('one_detail_edit'):
        session['detail'] = []
        detail_dict = []
        if request.values.get('one_detail_edit'):
            session['edit_detail_info'][0] = request.values.get('one_detail_edit')
            session['detail'].append(get_detail_name(conn, session['edit_detail_info'][0]))
            session['detail'].append(get_detail_size(conn, session['edit_detail_info'][0]))
            session['detail'].append(
                list(get_detail_measure(conn, session['edit_detail_info'][0]).loc[:, 'measure_name']))
            formula_list = get_detail_formula(conn, session['edit_detail_info'][0])['formula_name'].tolist()
            admin_panel_button = "Детали"
            for i in range(len(get_detail_lines(conn, session['edit_detail_info'][0]))):
                row = get_detail_lines(conn, session['edit_detail_info'][0]).iloc[i]
                session['detail_lines'].append([row['x_first_coord'], row['y_first_coord'], row['x_second_coord'],
                                                row['y_second_coord'], row['x_deviation'], row['y_deviation']])
            session['edit_detail_info'].append(session['detail'])
            session['edit_detail_info'].append(session['detail_lines'])
        else:
            session['detail'].append(request.values.get('new_detail_name'))
            session['detail'].append(request.values.get('new_detail_size'))
            session['detail'].append(request.values.getlist('new_detail_measure'))
            formula_list = request.values.getlist('new_detail_formula')

        for i in formula_list:
            detail_dict.append(get_formula(conn).loc[get_formula(conn)['formula_name'] == i].values[0][2])
        session['detail'].append(dict(zip(formula_list, detail_dict)))
        session['detail'][3] = dict(sorted(session['detail'][3].items()))
        session['detail'].append(session['edit_detail_info'][0])

        if is_correct_detail(conn, session['detail'][0], session['detail'][1], session['detail'][2],
                                 session['detail'][3]) != "True":
            admin_panel_button = "Детали"
            error_info = is_correct_detail(conn, session['detail'][0], session['detail'][1], session['detail'][2],
                                               session['detail'][3])

    elif request.values.get('add_detail_line') or request.values.get('edit_detail_line'):
        if request.values.get('edit_detail_line'):
            session['detail_lines'].pop(session['detail_lines'][len(session['detail_lines']) - 1][0])
            session['detail_lines'].pop(len(session['detail_lines']) - 1)
            admin_panel_button = "Просмотреть Список Линий"
        else:
            admin_panel_button = "Добавить Линии"
        session['detail_lines'].append([request.values.get('first_coord_x'), request.values.get('first_coord_y'),
                                        request.values.get('second_coord_x'), request.values.get('second_coord_y'),
                                        request.values.get('x_deviation'), request.values.get('y_deviation')])


    elif request.values.get('delete_detail_new_line'):
        line_id = int(request.values.get('delete_detail_new_line'))
        admin_panel_button = "Просмотреть Список Линий"
        session['detail_lines'].pop(line_id)

    elif request.values.get('edit_detail_new_line'):
        line_id = int(request.values.get('edit_detail_new_line'))
        admin_panel_button = "Добавить Линии"
        session['detail_lines'].append([line_id])


    elif admin_panel_button == "Просмотреть Схему":
        if session['edit_detail_info'] != ['']:
            update_detail(conn, session['edit_detail_info'][0], session['detail'][0], session['detail'][1])
            delete_detail(conn, session['edit_detail_info'][0], 'Обновление')
        else:
            add_detail(conn, session['detail'][0], session['detail'][1])

        detail_id = int(get_detail_id(conn, session["detail"][0]))
        for formula in session['detail'][3]:
            add_detail_formula(conn, detail_id, int(get_formula_id(conn, formula)))
        for measure in session['detail'][2]:
            add_detail_measure(conn, detail_id, int(get_measure_id(conn, measure)))
        for line in session['detail_lines']:
            add_detail_line(conn, detail_id, line)

        df_param = get_param_standard_w(conn)
        for index, row in df_param.iterrows():
            all_size_param = row['Значение'].split(",")
            row['Значение'] = float(all_size_param[2])

        value_list = []
        for i in session['detail'][2]:
            if i != "ДИ":
                value_list.append(df_param.loc[df_param['Обозначение'] == i].values[0][1])
            else:
                value_list.append(float(session['detail'][1]))
        df_param_detail = dict(zip(session['detail'][2], value_list))

        data = {'Обозначение': list(df_param_detail.keys()),
                'Значение': list(df_param_detail.values())}

        df_param_detail = pd.DataFrame(data)

        name_scheme = 'static/image/save_details/' + str(get_detail_name(conn, detail_id)) + '.jpg'
        pdf = PdfPages('static/pdf/admin.pdf')
        if is_correct_scheme(conn, df_param_detail, detail_id, pdf) == "True":
            create_user_scheme(conn, df_param_detail, detail_id, pdf)
        else:
            admin_panel_button = "Детали"
            error_info = is_correct_scheme(conn, df_param_detail, detail_id, pdf)

        pdf.close()
        if session['edit_detail_info'] == ['']:
            delete_detail(conn, int(get_detail_id(conn, session["detail"][0])), 'Удаление')

    elif request.values.get('add_new_detail'):
        if session['edit_detail_info'] == ['']:
            add_detail(conn, session['detail'][0], session['detail'][1])
            detail_id = int(get_detail_id(conn, session["detail"][0]))
            for formula in session['detail'][3]:
                add_detail_formula(conn, detail_id, int(get_formula_id(conn, formula)))
            for measure in session['detail'][2]:
                add_detail_measure(conn, detail_id, int(get_measure_id(conn, measure)))
            for line in session['detail_lines']:
                add_detail_line(conn, detail_id, line)
            os.remove('static/image/save_details/' + str(get_detail_name(conn, detail_id)) + '.jpg')
        session['detail'] = []
        session['detail_lines'] = []
        if session['edit_detail_info'] != ['']:
            admin_panel_button = "Список Деталей"
            os.remove(
                'static/image/save_details/' + str(get_detail_name(conn, session['edit_detail_info'][0])) + '.jpg')
            session['edit_detail_info'] = ['']
        else:
            admin_panel_button = "Детали"

    elif request.values.get('add_detail_cancel'):
        if session['edit_detail_info'] != ['']:
            detail_id = session['edit_detail_info'][0]
            update_detail(conn, detail_id, session['edit_detail_info'][1][0], session['edit_detail_info'][1][1])
            delete_detail(conn, session['edit_detail_info'][0], 'Обновление')
            for formula in session['edit_detail_info'][1][3]:
                add_detail_formula(conn, detail_id, int(get_formula_id(conn, formula)))
            for measure in session['edit_detail_info'][1][2]:
                add_detail_measure(conn, detail_id, int(get_measure_id(conn, measure)))
            for line in session['edit_detail_info'][2]:
                add_detail_line(conn, detail_id, line)

            admin_panel_button = "Список Деталей"
        else:
            admin_panel_button = "Детали"

        session['edit_detail_info'] = ['']
        session['detail'] = []
        session['detail_lines'] = []

    elif request.values.get('add_new_pattern'):
        name = request.values.get('new_pattern_name')
        picture = request.values.get('new_pattern_picture')
        category = request.values.get('new_pattern_category')
        difficulty = 0
        for detail in request.values.getlist('new_pattern_detail'):
            difficulty = difficulty + get_measure_number(conn, detail)

        if is_correct_pattern(conn, name, category, picture, request.values.getlist('new_pattern_detail')) == "True":
            add_pattern(conn, name,
                        picture, category, int(difficulty_calculation(get_category_by_id(conn, category),
                                                                      len(request.values.getlist('new_pattern_detail')),
                                                                      difficulty)))

            for detail in request.values.getlist('new_pattern_detail'):
                add_pattern_detail(conn, int(get_pattern_id(conn, name)), detail)
        else:
            error_info = is_correct_pattern(conn, name, category, picture, request.values.getlist('new_pattern_detail'))

        admin_panel_button = "Выкройки"

    elif request.values.get('one_pattern_info'):
        info_about_some = [int(request.values.get('one_pattern_info'))]
        info_about_some.append(get_detail_by_id(conn, info_about_some[0]).split(","))
        admin_panel_button = "Список Выкроек"

    elif request.values.get('one_pattern_edit'):
        info_about_some = [int(request.values.get('one_pattern_edit'))]
        info_about_some.append(get_detail_by_id(conn, info_about_some[0]).split(","))
        admin_panel_button = "Редактирование Выкроек"

    elif request.values.get('one_pattern_delete'):
        delete_pattern(conn, int(request.values.get('one_pattern_delete')))
        delete_pattern_detail(conn, int(request.values.get('one_pattern_delete')))
        admin_panel_button = "Список Выкроек"

    elif request.values.get('edit_pattern'):
        name = request.values.get('edit_pattern_name')
        picture = request.values.get('edit_pattern_picture')
        category = request.values.get('new_pattern_category')
        id = int(request.values.get('edit_pattern_id'))
        difficulty = 0
        for detail in request.values.getlist('new_pattern_detail'):
            difficulty = difficulty + get_measure_number(conn, detail)
        if is_correct_edit_pattern(conn, name, category, picture,
                                   request.values.getlist('new_pattern_detail')) == "True":
            update_pattern(conn, id, name, picture, category,
                           int(difficulty_calculation(get_category_by_id(conn, category),
                                                      len(request.values.getlist(
                                                          'new_pattern_detail')),
                                                      difficulty)))
            delete_pattern_detail(conn, id)
            for detail in request.values.getlist('new_pattern_detail'):
                add_pattern_detail(conn, id, detail)
            admin_panel_button = "Список Выкроек"
        else:
            error_info = is_correct_edit_pattern(conn, name, category, picture,
                                                 request.values.getlist('new_pattern_detail'))
            info_about_some = [int(request.values.get('edit_pattern_id'))]
            info_about_some.append(get_detail_by_id(conn, info_about_some[0]).split(","))
            admin_panel_button = "Редактирование Выкроек"

    elif request.values.get('add_pattern_cancel'):
        admin_panel_button = "Выкройки"

    elif request.values.get('edit_pattern_cancel'):
        admin_panel_button = "Список Выкроек"

    elif request.values.get('one_detail_info'):
        id = int(request.values.get('one_detail_info'))
        info_about_some = [get_detail_name(conn, id)]
        info_about_some.append(get_detail_size(conn, id))
        info_about_some.append(get_detail_measure(conn, id))
        info_about_some.append(get_detail_formula(conn, id))
        info_about_some.append(get_detail_lines(conn, id))
        admin_panel_button = "Список Деталей"

    elif request.values.get('one_detail_delete'):
        delete_detail(conn, int(request.values.get('one_detail_delete')), 'Удаление')
        admin_panel_button = "Список Деталей"

    df_detail = get_detail(conn)
    df_category = get_category(conn)
    df_formula = get_formula(conn)
    df_measure = get_measure(conn)
    df_line = get_line(conn)
    df_patterns = get_pattern(conn)
    html = render_template(
        'admin_profile.html',
        user_role=session['user_role'],
        admin_panel_button=admin_panel_button,
        category_list=df_category,
        checked_value=checked_value,
        formula_list=df_formula,
        measure_list=df_measure,
        line_list=df_line,
        detail_list=df_detail,
        pattern_list=df_patterns,
        new_detail_list=session['detail'],
        new_detail_line_list=session['detail_lines'],
        name_scheme=name_scheme,
        info_about_some=info_about_some,
        error_info=error_info,
        len=len
    )

    return html
