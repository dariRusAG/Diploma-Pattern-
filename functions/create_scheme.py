import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from models.model_general import get_detail_name
from models.scheme_model import *
from functions.bezie import Bezier
from PIL import Image


def setting_plt(value):
    plt.figure(figsize=(value / 2.54, value / 2.54))
    plt.xlim([0, value])
    plt.ylim([0, value])


# Инициализация параметров пользователя
def get_measurements(user_param):
    measure = {
        'ОГ': 0, 'ОТ': 0, 'ОБ': 0, 'ОШ': 0, 'ОПл': 0, 'ОЗ': 0,
        'ВБ': 0, 'ДИ': 0, 'ДТС': 0, 'ДПл': 0, 'ДЛ': 0
    }

    for item in measure.keys():
        if user_param['Обозначение'].eq(item).any():
            measure[item] = eval(user_param[user_param["Обозначение"] == item]["Значение"].values[0])

    ОГ, ОТ, ОБ, ОШ, ОПл, ОЗ, ВБ, ДИ, ДТС, ДПл, ДЛ = measure['ОГ'], measure['ОТ'], measure['ОБ'], \
        measure['ОШ'], measure['ОПл'], measure['ОЗ'], measure['ВБ'], measure['ДИ'], measure['ДТС'], \
        measure['ДПл'], measure['ДЛ']

    return ОГ, ОТ, ОБ, ОШ, ОПл, ОЗ, ВБ, ДИ, ДТС, ДПл, ДЛ

# Построение прямых линий
def build_line_straight(x_coord_line, y_coord_line):
    for i in range(0, len(x_coord_line) - 1, 2):
        plt.plot(
            [x_coord_line[i], x_coord_line[i + 1]],
            [y_coord_line[i], y_coord_line[i + 1]],
            c='black', lw=2.8
        )

# Построение кривых линий
def build_line_curve(curve, points):
    plt.plot(
        curve[:, 0],
        curve[:, 1], lw=2.8
    )

    # Точки для безье
    plt.plot(
        points[:, 0],
        points[:, 1],
        'ro:',
        color='darkblue'
    )

# Расчет координат кривых линий
def calculate_line_curve(row, x_coord_line, y_coord_line, df_formula):
    # список всех x и y отклонений кривых линий
    x_deviation = list()
    y_deviation = list()

    # Если отклонений несколько, то преобразование в список
    if type(eval(f"{row['x_deviation']}")) == float or type(eval(f"{row['x_deviation']}")) == int:
        x1_deviation = eval(f"{row['x_deviation']}", {}, df_formula)
    else:
        x1_deviation = f"{row['x_deviation']}".split(",")
        for num in range(len(x1_deviation)):
            x1_deviation[num] = float(x1_deviation[num])
    if type(eval(f"{row['y_deviation']}")) == float or type(eval(f"{row['y_deviation']}")) == int:
        y1_deviation = eval(f"{row['y_deviation']}", {}, df_formula)
    else:
        y1_deviation = f"{row['y_deviation']}".split(",")
        for num in range(len(y1_deviation)):
            y1_deviation[num] = float(y1_deviation[num])

    x_deviation.append(x1_deviation)
    y_deviation.append(y1_deviation)

    # Построение линий
    for i in range(0, len(x_coord_line) - 1, 2):
        t_points = np.arange(0, 1, 0.009)

        j = int(i / 2)
        list_new_x = []
        list_new_y = []

        # если отклонение одно
        if type(x_deviation[j]) == float or type(x_deviation[j]) == int:
            d_x_first = x_deviation[j]
            d_y_first = y_deviation[j]

            list_new_x.append(((x_coord_line[i] + x_coord_line[i + 1]) / 2) * d_x_first)
            list_new_y.append(((y_coord_line[i] + y_coord_line[i + 1]) / 2) * d_y_first)

        # если отклонений несколько
        else:
            k = len(x_deviation[j])
            for r in range(1, k + 1):
                d_x_first = x_deviation[j][r - 1]
                d_y_first = y_deviation[j][r - 1]

                # формула расчета координат в отношении
                alpha = r / (k + 1 - r)
                list_new_x.append(((x_coord_line[i] + alpha * x_coord_line[i + 1]) / (1 + alpha)) * d_x_first)
                list_new_y.append(((y_coord_line[i] + alpha * y_coord_line[i + 1]) / (1 + alpha)) * d_y_first)

        # список всех отклонений прямой
        all_deviations = []
        for j in range(len(list_new_x)):
            all_deviations.append([list_new_x[j], list_new_y[j]])

        # список всех точек для построения
        points_list = [[x_coord_line[i], y_coord_line[i]]]
        points_list = points_list + all_deviations
        points_list.append(
            [x_coord_line[i + 1], y_coord_line[i + 1]]
        )
        points1 = np.asarray(points_list)

    curve1 = Bezier.Curve(t_points, points1)
    return curve1, points1


def create_user_scheme(conn, user_param, id_detail):
    # создание словаря формул
    df_formula = get_formula_detail(conn, id_detail)
    df_formula = df_formula.set_index('formula_name').T.to_dict('list')

    # получение мерок выкроек
    ОГ, ОТ, ОБ, ОШ, ОПл, ОЗ, ВБ, ДИ, ДТС, ДПл, ДЛ = get_measurements(user_param)

    measurements = {
        'ОГ': ОГ, 'ОТ': ОТ, 'ОБ': ОБ, 'ОШ': ОШ, 'ОПл': ОПл, 'ОЗ': ОЗ,
        'ВБ': ВБ, 'ДИ': ДИ, 'ДТС': ДТС, 'ДПл': ДПл, 'ДЛ': ДЛ
    }

    # расчёт всех формул в зависимости от значений мерок
    for formula in df_formula:
        df_formula[formula] = eval(eval(formula, measurements, df_formula)[0])

    # if measurements['ДИ'] != 0:
    #     setting_plt(measurements['ДИ'])
    # elif measurements['ОПл'] != 0:
    #     setting_plt(measurements['ОПл'] + 5)
    # else:
    #     setting_plt(measurements['ОШ'] / 2)

    # получение всех линий
    df_line = get_line_detail(conn, id_detail)

    x_coord_line_straight = []
    y_coord_line_straight = []
    line_curve = []
    line_curve_points = []

    # Список всех координат линий
    x_list = []
    y_list = []

    # Расчёт координат линий
    for index, row in df_line.iterrows():
        # список всех x и y координат прямых линий
        x_coord_line = list()
        y_coord_line = list()

        x1 = eval(f"{row['x_first_coord']}", measurements, df_formula)
        y1 = eval(f"{row['y_first_coord']}", measurements, df_formula)

        x2 = eval(f"{row['x_second_coord']}", measurements, df_formula)
        y2 = eval(f"{row['y_second_coord']}", measurements, df_formula)

        x_coord_line.append(x1)
        y_coord_line.append(y1)
        x_coord_line.append(x2)
        y_coord_line.append(y2)

        if df_line.loc[index, 'x_deviation'] == '':
            x_coord_line_straight.append(x_coord_line)
            y_coord_line_straight.append(y_coord_line)
        else:
            curve, points_curve = calculate_line_curve(row, x_coord_line, y_coord_line, df_formula)
            line_curve.append(curve)
            line_curve_points.append(points_curve)
            for coord in curve:
                x_list.append(coord[0])
                y_list.append(coord[1])

        x_list += x_coord_line
        y_list += y_coord_line

    length_x = max(x_list) - min(x_list)
    length_y = max(y_list) - min(y_list)

    # Определение масштаба схемы
    if length_x >= length_y:
        setting_plt(length_x + 2)
    else:
        setting_plt(length_y + 2)

    # Построение всех линий
    for x_straight, y_straight in zip(x_coord_line_straight, y_coord_line_straight):
        build_line_straight(x_straight, y_straight)
    for curves, curves_points in zip(line_curve, line_curve_points):
        build_line_curve(curves, curves_points)

    name = 'static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg'

    plt.savefig(name, bbox_inches='tight')
    Image.open(name).save(name)

    # количество листов по иксу
    pages_x = math.ceil(length_x / 21)
    # количество листов по игреку
    pages_y = math.ceil(length_y / 29.7)

    # сохранение в формате А4
    pdf = PdfPages('static/pdf/' + str(get_detail_name(conn, id_detail)) + '.pdf')

    for i in range(pages_y):
        y = 1 + 29.7 * i
        for j in range(pages_x):
            x = 1 + 21 * j
            add_to_pdf(pdf, x, x + 21, y, y + 29.7)

            # # Удаление пустых листов А4
            # for coord_x, coord_y in zip(x_list, y_list):
            #     if (x <= coord_x < x + 21) and (y <= coord_y < y + 29.7):
            #         add_to_pdf(pdf, x, x + 21, y, y + 29.7)
            #         break

    pdf.close()


def add_to_pdf(pdf, x1, x2, y1, y2):
    plt.axis('off')
    plt.xlim([x1, x2])
    plt.ylim([y1, y2])
    pdf.savefig(bbox_inches='tight')
