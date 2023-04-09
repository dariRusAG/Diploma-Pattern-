import matplotlib.pyplot as plt
import bezier
import numpy as np
from models.admin_profile_model import *


def get_plot(x_up, y_up, x_down, y_down, otstup_a, otstup_b):
    P1 = np.array([x_up, y_up])
    P2 = np.array([x_down, y_down])
    P3 = P2 + (P1 - P2) * np.array([otstup_a, otstup_b])
    nodes1 = np.asfortranarray([
        [P1[0], P3[0], P2[0]],
        [P1[1], P3[1], P2[1]],
    ])
    curve = bezier.Curve(nodes1, degree=2)
    xx = np.linspace(0, 1, 10)
    yy = map(lambda x: curve.evaluate(x), xx)
    x_ = []
    y_ = []
    for _ in np.array(list(yy)):
        x_.append(_[0])
        y_.append(_[1])
    return [x_, y_]


def create_user_scheme(conn):
    # список всех формул
    df_formula = get_formula(conn)
    # список всех линий
    df_line = get_line(conn)
    # создание словаря формул
    df_formula = df_formula.set_index('formula_name').T.to_dict('list')
    # мерки выкроек
    dlina_izd = 80
    obhvat_bed_1 = 120
    vusota_bed = 40
    obhvat_t = 82
    measurements = {'dlina_izd': dlina_izd, 'obhvat_bed_1': obhvat_bed_1, 'vusota_bed': vusota_bed,
                    'obhvat_t': obhvat_t}

    # расчёт всех формул в зависимости от значений мерок
    for formula in df_formula:
        df_formula[formula] = eval(eval(formula, {}, df_formula)[0])

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
            y_deviation_ = eval(f"{row['x_deviation']}", {}, df_formula)
            x_coord_curve.append(x1)
            y_coord_curve.append(y1)
            x_coord_curve.append(x2)
            y_coord_curve.append(y2)
            design_for_curve.append(curve_design)
            x_deviation.append(x_deviation_)
            y_deviation.append(y_deviation_)

    # построение линий в зависимости от их типа
    for x in range(0, len(x_coord_line) - 1, 2):
        if design_for_line[int(x / 2)] == "normal":
            plt.plot([x_coord_line[x], x_coord_line[x + 1]], [y_coord_line[x], y_coord_line[x + 1]],
                     c='black', lw=0.8)
        else:
            plt.plot([x_coord_line[x], x_coord_line[x + 1]], [y_coord_line[x], y_coord_line[x + 1]],
                     c='black', ls='-.', lw=0.8)

    for x in range(0, len(x_coord_curve) - 1, 2):
        if design_for_line[int(x / 2)] == "normal":
            curve = get_plot(x_coord_curve[x], x_coord_curve[x + 1], y_coord_curve[x], y_coord_curve[x + 1],
                             x_deviation[int(x / 2)], y_deviation[int(x / 2)])
            plt.plot(curve[0], curve[1], c='black', lw=0.8)
        else:
            curve = get_plot(x_coord_curve[x], x_coord_curve[x + 1], y_coord_curve[x], y_coord_curve[x + 1],
                             x_deviation[int(x / 2)], y_deviation[int(x / 2)])
            plt.plot(curve[0], curve[1], c='black', ls='-.', lw=0.8)

    plt.legend
    plt.xlim([0, dlina_izd])
    plt.ylim([0, dlina_izd + 5])
    plt.savefig("pict.jpg")
