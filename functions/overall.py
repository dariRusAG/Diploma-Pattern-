from flask import session, request
from models.catalog_favorites_model import *


def favorites_pattern(conn, category, complexity):
    if request.values.get('empty'):
        choice_favorite_pattern = request.values.get('pattern')
        if (choice_favorite_pattern != 0) or ('user_id' in session):
            add_pattern(conn, session['user_id'], choice_favorite_pattern)

    elif request.values.get('shaded'):
        choice_favorite_pattern = request.values.get('pattern')
        if (choice_favorite_pattern != 0) or ('user_id' in session):
            del_pattern(conn, choice_favorite_pattern)

    if 'user_id' not in session:
        user_id = 0
    else:
        user_id = session['user_id']

    df_favorite_pattern = get_favorite_pattern(conn, user_id, category, complexity)

    favorite_list = []
    for i in range(len(df_favorite_pattern)):
        favorite_list.append(df_favorite_pattern.loc[i, "ID"])

    return df_favorite_pattern, favorite_list


def get_measurements(user_param):
    ОГ = 0
    ОТ = 0
    ОБ = 0
    ОШ = 0
    ОПл = 0
    ОЗ = 0
    ВБ = 0
    ДИ = 0
    ДТС = 0
    ДПл = 0
    ДР = 0

    if user_param['Обозначение'].eq('ОГ').any():
        ОГ = eval(user_param[user_param["Обозначение"] == 'ОГ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ОТ').any():
        ОТ = eval(user_param[user_param["Обозначение"] == 'ОТ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ОБ').any():
        ОБ = eval(user_param[user_param["Обозначение"] == 'ОБ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ОШ').any():
        ОШ = eval(user_param[user_param["Обозначение"] == 'ОШ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ОПл').any():
        ОПл = eval(user_param[user_param["Обозначение"] == 'ОПл']["Значение"].values[0])
    if user_param['Обозначение'].eq('ОЗ').any():
        ОЗ = eval(user_param[user_param["Обозначение"] == 'ОЗ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ВБ').any():
        ВБ = eval(user_param[user_param["Обозначение"] == 'ВБ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ДИ').any():
        ДИ = eval(user_param[user_param["Обозначение"] == 'ДИ']["Значение"].values[0])
    if user_param['Обозначение'].eq('ДТС').any():
        ДТС = eval(user_param[user_param["Обозначение"] == 'ДТС']["Значение"].values[0])
    if user_param['Обозначение'].eq('ДПл').any():
        ДПл = eval(user_param[user_param["Обозначение"] == 'ДПл']["Значение"].values[0])
    if user_param['Обозначение'].eq('ДР').any():
        ДР = eval(user_param[user_param["Обозначение"] == 'ДР']["Значение"].values[0])

    return ОГ, ОТ, ОБ, ОШ, ОПл, ОЗ, ВБ, ДИ, ДТС, ДПл, ДР
