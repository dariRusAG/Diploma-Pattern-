import matplotlib.pyplot as plt
import numpy as np
from models.scheme_model import *
from functions.bezie import Bezier
from PIL import Image


def cm_to_inch(value):
    return value / 2.54


# Инициализация параметров пользователя
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


# Подсчет координат линий и их построение
def build_line_curve(df_line_curve, difficult, measurements, df_formula):
    design_for_curve = list()

    # список всех x и y координат кривых линий
    x_coord_curve = list()
    y_coord_curve = list()

    # список всех x и y отклонений кривых линий
    x_deviation = list()
    y_deviation = list()

    # Расчет координат линий
    for index, row in df_line_curve.iterrows():
        x1 = eval(f"{row['x_first_coord']}", measurements, df_formula)
        y1 = eval(f"{row['y_first_coord']}", measurements, df_formula)

        x2 = eval(f"{row['x_second_coord']}", measurements, df_formula)
        y2 = eval(f"{row['y_second_coord']}", measurements, df_formula)

        x1_deviation = eval(f"{row['x_first_deviation']}", {}, df_formula)
        y1_deviation = eval(f"{row['y_first_deviation']}", {}, df_formula)

        x_coord_curve.append(x1)
        y_coord_curve.append(y1)
        x_coord_curve.append(x2)
        y_coord_curve.append(y2)

        x_deviation.append(x1_deviation)
        y_deviation.append(y1_deviation)

        if difficult == 'complex':
            x2_deviation = eval(f"{row['x_second_deviation']}", {}, df_formula)
            y2_deviation = eval(f"{row['y_second_deviation']}", {}, df_formula)
            x_deviation.append(x2_deviation)
            y_deviation.append(y2_deviation)

        # список стилей кривых линий
        curve_design = f"{row['line_design']}"
        design_for_curve.append(curve_design)

        # Построение линий
        for i in range(0, len(x_coord_curve) - 1, 2):
            t_points = np.arange(0, 1, 0.009)

            if difficult == 'simple':
                d_x = x_deviation[int(i / 2)]
                d_y = y_deviation[int(i / 2)]

                deviation_middle_X = ((x_coord_curve[i] + x_coord_curve[i + 1]) / 2) * d_x
                deviation_middle_Y = ((y_coord_curve[i] + y_coord_curve[i + 1]) / 2) * d_y

                points1 = np.array(
                    [
                        [x_coord_curve[i], y_coord_curve[i]],
                        [deviation_middle_X, deviation_middle_Y],
                        [x_coord_curve[i + 1], y_coord_curve[i + 1]]
                    ])

            elif difficult == 'complex':
                d_x_first = x_deviation[int(i)]
                d_y_first = y_deviation[int(i)]

                deviation_first_X = ((x_coord_curve[i] + x_coord_curve[i + 1]) / 3) * d_x_first
                deviation_first_Y = ((y_coord_curve[i] + y_coord_curve[i + 1]) / 3) * d_y_first

                d_x_second = x_deviation[int(i + 1)]
                d_y_second = y_deviation[int(i + 1)]

                deviation_second_X = ((x_coord_curve[i] + x_coord_curve[i + 1]) / 1.5) * d_x_second
                deviation_second_Y = ((y_coord_curve[i] + y_coord_curve[i + 1]) / 1.5) * d_y_second

                points1 = np.array(
                    [
                        [x_coord_curve[i], y_coord_curve[i]],
                        [deviation_first_X, deviation_first_Y],
                        [deviation_second_X, deviation_second_Y],
                        [x_coord_curve[i + 1], y_coord_curve[i + 1]]
                    ])

        curve1 = Bezier.Curve(t_points, points1)
        plt.plot(
            curve1[:, 0],
            curve1[:, 1], lw=2.8
        )


def create_user_scheme(conn, user_param, id_detail):
    # создание словаря формул
    df_formula = get_formula_detail(conn, id_detail)
    df_formula = df_formula.set_index('formula_name').T.to_dict('list')

    # получение мерок выкроек
    ОГ, ОТ, ОБ, ОШ, ОПл, ОЗ, ВБ, ДИ, ДТС, ДПл, ДР = get_measurements(user_param)

    measurements = {
        'ОГ': ОГ, 'ОТ': ОТ, 'ОБ': ОБ, 'ОШ': ОШ, 'ОПл': ОПл, 'ОЗ': ОЗ,
        'ВБ': ВБ, 'ДИ': ДИ, 'ДТС': ДТС, 'ДПл': ДПл, 'ДР': ДР
    }

    # расчёт всех формул в зависимости от значений мерок
    for formula in df_formula:
        df_formula[formula] = eval(eval(formula, measurements, df_formula)[0])

    # список всех x и y координат прямых линий
    x_coord_line = list()
    y_coord_line = list()

    # список стилей прямых линий
    design_for_line = list()

    # получение всех линий
    df_line_straight = get_line_straight_detail(conn, id_detail)
    df_line_curve = get_line_curve_detail(conn, id_detail)

    if id_detail == 4:
        plt.figure(figsize=(cm_to_inch(ДР), cm_to_inch(ДР + 5)))
    else:
        plt.figure(figsize=(cm_to_inch(ДИ), cm_to_inch(ДИ + 5)))

    # Расчёт координат прямых линий
    for index, row in df_line_straight.iterrows():
        x1 = eval(f"{row['x_first_coord']}", measurements, df_formula)
        y1 = eval(f"{row['y_first_coord']}", measurements, df_formula)

        x2 = eval(f"{row['x_second_coord']}", measurements, df_formula)
        y2 = eval(f"{row['y_second_coord']}", measurements, df_formula)

        line_design = f"{row['line_design']}"
        design_for_line.append(line_design)

        x_coord_line.append(x1)
        y_coord_line.append(y1)
        x_coord_line.append(x2)
        y_coord_line.append(y2)

    # Построение прямых линий
    for i in range(0, len(x_coord_line) - 1, 2):
        if design_for_line[int(i / 2)] == "Обычная":
            plt.plot(
                [x_coord_line[i], x_coord_line[i + 1]],
                [y_coord_line[i], y_coord_line[i + 1]],
                c='black', lw=2.8
            )
        elif design_for_line[int(i / 2)] == "Пунктир":
            plt.plot(
                [x_coord_line[i], x_coord_line[i + 1]],
                [y_coord_line[i], y_coord_line[i + 1]],
                c='black', ls='-.', lw=2.8
            )

    df_line_curve_simple = df_line_curve.loc[(df_line_curve['x_second_deviation'] == '')]
    df_line_curve_complex = df_line_curve.loc[(df_line_curve['x_second_deviation'] != '')]

    build_line_curve(df_line_curve_simple, 'simple', measurements, df_formula)
    build_line_curve(df_line_curve_complex, 'complex', measurements, df_formula)

    if id_detail == 4:
        plt.xlim([0, ДР])
        plt.ylim([0, ДР + 5])
    else:
        plt.xlim([0, ДИ])
        plt.ylim([0, ДИ + 5])

    # ax = plt.gca()
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)

    name = 'static/' + str(id_detail) + '.jpg'

    plt.savefig(name, bbox_inches='tight')
    im = Image.open(name)
    im.save(name)

    # im.crop((0, 0, im.size[0] - im.size[0] * 0.50, im.size[1])).save(name)

