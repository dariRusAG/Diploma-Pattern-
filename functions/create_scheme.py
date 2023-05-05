import matplotlib.pyplot as plt
import numpy as np
from models.scheme_model import *
from functions.overall import get_measurements
from functions.bezie import Bezier
from PIL import Image


def cm_to_inch(value):
    return value / 2.54


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

    # список всех x и y координат кривых линий
    x_coord_curve = list()
    y_coord_curve = list()

    # список всех x и y отклонений для кривых
    x_deviation = list()
    y_deviation = list()

    # список всех стилей прямых и кривых линий
    design_for_line = list()
    design_for_curve = list()

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
        x_coord_line.append(x1)
        y_coord_line.append(y1)
        x_coord_line.append(x2)
        y_coord_line.append(y2)
        design_for_line.append(line_design)

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

    # Расчёт координат кривых линий
    for index, row in df_line_curve.iterrows():
        curve_design = f"{row['line_design']}"

        x1 = eval(f"{row['x_first_coord']}", measurements, df_formula)
        y1 = eval(f"{row['y_first_coord']}", measurements, df_formula)

        x2 = eval(f"{row['x_second_coord']}", measurements, df_formula)
        y2 = eval(f"{row['y_second_coord']}", measurements, df_formula)

        x1_deviation = eval(f"{row['x_first_deviation']}", {}, df_formula)
        y1_deviation = eval(f"{row['y_first_deviation']}", {}, df_formula)

        if df_line_curve.loc[index, 'x_third_coord'] != '' or df_line_curve.loc[index, 'y_third_coord'] != '':
            x3 = eval(f"{row['x_third_coord']}", measurements, df_formula)
            y3 = eval(f"{row['y_third_coord']}", measurements, df_formula)

            x2_deviation = eval(f"{row['x_second_deviation']}", {}, df_formula)
            y2_deviation = eval(f"{row['y_second_deviation']}", {}, df_formula)
        else:
            x3 = ''
            y3 = ''
            x2_deviation = ''
            y2_deviation = ''

        x_coord_curve.append(x1)
        y_coord_curve.append(y1)
        x_coord_curve.append(x2)
        y_coord_curve.append(y2)

        x_deviation.append(x1_deviation)
        y_deviation.append(y1_deviation)

        design_for_curve.append(curve_design)

        if x3 != '' or y3 != '':
            x_coord_curve.append(x3)
            y_coord_curve.append(y3)

            x_deviation.append(x2_deviation)
            y_deviation.append(y2_deviation)

    # Построение кривых линий
    for i in range(0, len(x_coord_curve) - 1, 2):
        t_points = np.arange(0, 1, 0.009)

        if len(x_coord_curve) == len(x_deviation):
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
        else:
            d_x = x_deviation[int(i / 2)]
            d_y = y_deviation[int(i / 2)]

            deviation_middle_X = ((x_coord_curve[i] + x_coord_curve[i + 1]) / 2) * d_x
            deviation_middle_Y = ((y_coord_curve[i] + y_coord_curve[i + 1]) / 2) * d_y

            points1 = np.array(
                [[x_coord_curve[i], y_coord_curve[i]], [deviation_middle_X, deviation_middle_Y],
                 [x_coord_curve[i + 1], y_coord_curve[i + 1]]])

        curve1 = Bezier.Curve(t_points, points1)
        plt.plot(
            curve1[:, 0],
            curve1[:, 1], lw=2.8
        )

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

