import matplotlib.pyplot as plt
import numpy as np
from models.admin_profile_model import *
from functions.bezie import Bezier
from PIL import Image

def cm_to_inch(value):
  return value/2.54

def create_user_scheme(conn, user_param):
    # список всех формул
    df_formula = get_formula(conn)
    # список всех линий
    df_line = get_line(conn)
    # создание словаря формул
    df_formula = df_formula.set_index('formula_name').T.to_dict('list')
    # мерки выкроек
    ДИ = eval(user_param[user_param["Обозначение"] == 'ДИ']["Значение"].values[0])
    ОБ = eval(user_param[user_param["Обозначение"] == 'ОБ']["Значение"].values[0])
    ВБ = eval(user_param[user_param["Обозначение"] == 'ВБ']["Значение"].values[0])
    ОТ = eval(user_param[user_param["Обозначение"] == 'ОТ']["Значение"].values[0])

    measurements = {'ДИ': ДИ, 'ОБ': ОБ, 'ВБ': ВБ,
                    'ОТ': ОТ}

    # расчёт всех формул в зависимости от значений мерок
    for formula in df_formula:
        df_formula[formula] = eval(eval(formula, measurements, df_formula)[0])

    # список всех x координат прямых линий
    x_coord_line = list()
    # список всех y координат прямых линий
    y_coord_line = list()
    # список всех x координат прямых линий
    x_coord_curve = list()
    # список всех y координат прямых линий
    y_coord_curve = list()
    # список всех x отклонений для кривых
    x_deviation = list()
    # список всех y отклонений для кривых
    y_deviation = list()
    # список всех стилей прямых линий
    design_for_line = list()
    # список всех стилей кривых линий
    design_for_curve = list()

    # расчёт координат линий
    for i, row in df_line.iterrows():
        x1 = eval(f"{row['x_first_coord']}", measurements, df_formula)
        y1 = eval(f"{row['y_first_coord']}", measurements, df_formula)

        x2 = eval(f"{row['x_second_coord']}", measurements, df_formula)
        y2 = eval(f"{row['y_second_coord']}", measurements, df_formula)
        if f"{row['line_type']}" != "curve":
            line_design = f"{row['line_design']}"
            x_coord_line.append(x1)
            y_coord_line.append(y1)
            x_coord_line.append(x2)
            y_coord_line.append(y2)
            design_for_line.append(line_design)
        else:
            curve_design = f"{row['line_design']}"
            x_deviation_ = eval(f"{row['x_deviation']}", {}, df_formula)
            y_deviation_ = eval(f"{row['y_deviation']}", {}, df_formula)
            x_coord_curve.append(x1)
            y_coord_curve.append(y1)
            x_coord_curve.append(x2)
            y_coord_curve.append(y2)
            design_for_curve.append(curve_design)
            x_deviation.append(x_deviation_)
            y_deviation.append(y_deviation_)

    plt.figure(figsize=(cm_to_inch(ДИ), cm_to_inch(ДИ + 5)))

    # построение линий в зависимости от их типа
    for x in range(0, len(x_coord_line) - 1, 2):
        if design_for_line[int(x / 2)] == "normal":
            plt.plot([x_coord_line[x], x_coord_line[x + 1]], [y_coord_line[x], y_coord_line[x + 1]],
                     c='black', lw=2.8)
        else:
            plt.plot([x_coord_line[x], x_coord_line[x + 1]], [y_coord_line[x], y_coord_line[x + 1]],
                     c='black', ls='-.', lw=2.8)

    for x in range(0, len(x_coord_curve) - 1, 2):
        t_points = np.arange(0, 1, 0.009)
        d_x = x_deviation[int(x / 2)]
        d_y = y_deviation[int(x / 2)]
        k= ((x_coord_curve[x] + x_coord_curve[x+1])/2) * d_x
        kk=((y_coord_curve[x] + y_coord_curve[x + 1])/2) * d_y
        points1 = np.array([[x_coord_curve[x], y_coord_curve[x]], [k, kk], [x_coord_curve[x + 1], y_coord_curve[x + 1]]])
        curve1 = Bezier.Curve(t_points, points1)
        plt.plot(
            curve1[:, 0],
            curve1[:, 1], lw=2.8
        )


    plt.xlim([0, ДИ])
    plt.ylim([0, ДИ + 5])
    # ax = plt.gca()
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    plt.savefig("static/scheme.jpg", bbox_inches='tight')
    im = Image.open('static/scheme.jpg')
    im.crop((0, 0, im.size[0]-im.size[0]*0.50, im.size[1])).save('static/scheme.jpg')
