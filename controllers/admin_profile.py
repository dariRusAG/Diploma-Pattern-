from app import app
from flask import render_template, request, session
from models.admin_profile_model import *
from models.model_general import get_detail_name
from utils import get_db_connection
from functions.create_scheme import *
import os


# Подсчет сложности выкройки
def difficulty_calculation(category, number_details, number_measurements):
    complexity = number_details * number_measurements

    match category:
        case 'Юбки':
            complexity *= 1
        case 'Футболки', 'Брюки':
            complexity *= 2
        case 'Рубашки':
            complexity *= 3
        case 'Платья':
            complexity *= 4

    match complexity:
        case [2, 40]:
            complexity = 1
        case [41, 78]:
            complexity = 2
        case [79, 116]:
            complexity = 3
        case [117, 154]:
            complexity = 4
        case [155, 192]:
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
    pattern_info = ['', '']

    if 'detail' not in session:
        session['detail'] = []
    if 'detail_lines' not in session:
        session['detail_lines'] = []

    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    if request.values.get('add_category'):
        if get_category_id(conn, request.values.get('new_category')) == "error" and request.values.get(
                'new_category') != '':
            add_category(conn, request.values.get('new_category'))
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
        if get_category_id(conn, request.values.get('edit_category_name')) == "error" and request.values.get(
                'edit_category_name') != '':
            category_name = request.values.get('edit_category_name')
            update_category(conn, category_id, category_name)
        checked_value = False
        admin_panel_button = "Категории"

    elif request.values.get('add_formula'):
        if get_formula_id(conn, request.values.get('new_formula_name'),
                          request.values.get('new_formula_value')) == "error" \
                and request.values.get('new_formula_name') != '' and request.values.get('new_formula_value') != '':
            add_formula(conn, request.values.get('new_formula_name'), request.values.get('new_formula_value'))
        admin_panel_button = "Формулы"

    elif admin_panel_button == "Добавить Линии":
        session['detail'] = []
        session['detail'].append(request.values.get('new_detail_name'))
        session['detail'].append(request.values.getlist('new_detail_measure'))
        detail_dict = []
        for i in request.values.getlist('new_detail_formula'):
            detail_dict.append(get_formula(conn).loc[get_formula(conn)['formula_name'] == i].values[0][1])
        session['detail'].append(dict(zip(request.values.getlist('new_detail_formula'), detail_dict)))
        session['detail'][2] = dict(sorted(session['detail'][2].items()))

    elif request.values.get('add_detail_line') or request.values.get('edit_detail_line'):
        if request.values.get('edit_detail_line'):
            session['detail_lines'].pop(session['detail_lines'][len(session['detail_lines']) - 1][0])
            session['detail_lines'].pop(len(session['detail_lines']) - 1)
            admin_panel_button = "Просмотреть Список Линий"
        else:
            admin_panel_button = "Добавить Линии"
        session['detail_lines'].append([request.values.get('first_coord_x'), request.values.get('first_coord_y'),
                                        request.values.get('second_coord_x'), request.values.get('second_coord_y'),
                                        request.values.get('x_deviation'), request.values.get('y_deviation'),
                                        request.values.get('line_design')])


    elif request.values.get('delete_detail_new_line'):
        line_id = int(request.values.get('delete_detail_new_line'))
        admin_panel_button = "Просмотреть Список Линий"
        session['detail_lines'].pop(line_id)

    elif request.values.get('edit_detail_new_line'):
        line_id = int(request.values.get('edit_detail_new_line'))
        admin_panel_button = "Добавить Линии"
        session['detail_lines'].append([line_id])


    elif admin_panel_button == "Просмотреть Схему":
        add_detail(conn, session['detail'][0])
        detail_id = int(get_detail_id(conn, session["detail"][0]))
        for formula in session['detail'][2]:
            add_detail_formula(conn, detail_id, int(get_formula_id(conn, formula)))
        for measure in session['detail'][1]:
            add_detail_measure(conn, detail_id, int(get_measure_id(conn, measure)))
        for line in session['detail_lines']:
            add_detail_line(conn, detail_id, line)

        # ИСПРАВИТЬ!!!
        data = {'Обозначение': ['ОГ', 'ОТ', 'ОБ', 'ОШ', 'ОПл', 'ОЗ',
                                'ВБ', 'ДИ', 'ДТС', 'ДПл', 'ДР'],
                'Значение': [str(108), str(89), str(94), str(37), str(34), str(17), str(45),
                             str(80), str(45), str(18), str(65)]}
        df_param_detail = pd.DataFrame(data)
        name_scheme = 'static/' + str(get_detail_name(conn, detail_id)) + '.jpg'
        create_user_scheme(conn, df_param_detail, detail_id)
        delete_new_detail(conn, int(get_detail_id(conn, session["detail"][0])))


    elif request.values.get('add_new_detail'):
        add_detail(conn, session['detail'][0])
        detail_id = int(get_detail_id(conn, session["detail"][0]))
        for formula in session['detail'][2]:
            add_detail_formula(conn, detail_id, int(get_formula_id(conn, formula)))
        for measure in session['detail'][1]:
            add_detail_measure(conn, detail_id, int(get_measure_id(conn, measure)))
        for line in session['detail_lines']:
            add_detail_line(conn, detail_id, line)
        session['detail'] = []
        session['detail_lines'] = []
        os.remove('static/' + str(get_detail_name(conn, detail_id)) + '.jpg')
        admin_panel_button = "Детали"

    elif request.values.get('add_detail_cancel'):
        session['detail'] = []
        session['detail_lines'] = []
        admin_panel_button = "Детали"

    elif request.values.get('add_new_pattern'):
        name = request.values.get('new_pattern_name')
        picture = request.values.get('new_pattern_picture')
        category = request.values.get('new_pattern_category')
        add_pattern(conn, name, picture, category, 5)
        for detail in request.values.getlist('new_pattern_detail'):
            add_pattern_detail(conn, int(get_pattern_id(conn, name)), detail)
        admin_panel_button = "Выкройки"

    elif request.values.get('one_pattern_info'):
        pattern_info = [int(request.values.get('one_pattern_info')) - 1]
        pattern_info.append(get_detail_by_id(conn, pattern_info[0] + 1).split(","))
        admin_panel_button = "Список Выкроек"

    elif request.values.get('one_pattern_edit'):
        pattern_info = [int(request.values.get('one_pattern_edit')) - 1]
        pattern_info.append(get_detail_by_id(conn, pattern_info[0] + 1).split(","))
        admin_panel_button = "Редактирование Выкроек"

    elif request.values.get('edit_pattern'):
        name = request.values.get('edit_pattern_name')
        picture = request.values.get('edit_pattern_picture')
        category = request.values.get('new_pattern_category')
        id = int(request.values.get('edit_pattern_id')) + 1
        update_pattern(conn, id, name, picture, category)
        delete_pattern_detail(conn, id)
        for detail in request.values.getlist('new_pattern_detail'):
            add_pattern_detail(conn, id, detail)
        admin_panel_button = "Список Выкроек"

    elif request.values.get('add_pattern_cancel'):
        admin_panel_button = "Выкройки"

    elif request.values.get('edit_pattern_cancel'):
        admin_panel_button = "Список Выкроек"

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
        pattern_info=pattern_info,
        len=len
    )

    return html
