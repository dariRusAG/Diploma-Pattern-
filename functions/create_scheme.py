import math
import matplotlib.pyplot as plt
import numpy as np
from models.scheme_model import *
from functions.bezie import Bezier
from matplotlib.backends.backend_pdf import PdfPages


def setting_plt(value):
    plt.figure(figsize=(value / 2.54, value / 2.54))
    plt.xlim([0, value])
    plt.ylim([0, value])


# Построение прямых линий
def build_line_straight(x_coord_line, y_coord_line, func_name, i):

    plt.plot(
        [x_coord_line[0], x_coord_line[1]],
        [y_coord_line[0], y_coord_line[1]],
        c='black', lw=2.8
    )
    if func_name == "admin":
        xmean = (x_coord_line[0] + x_coord_line[1]) / 2
        ymean = (y_coord_line[0] + y_coord_line[1]) / 2
        plt.annotate("Прямая - " + str(i), xy=(xmean + 0.2, ymean + 0.2), xycoords='data')


# Построение кривых линий
def build_line_curve(curve, points, func_name, i):
    if func_name == "admin":
        plt.plot(
            curve[:, 0],
            curve[:, 1], lw=2.8
        )
        curve_x = points[:, 0]
        curve_y = points[:, 1]
        xmean = (curve_x[0] + curve_x[len(curve_x)-1] + curve_x[int(len(curve_x) / 2)]) / 3
        ymean = (curve_y[0] + curve_y[len(curve_y)-1] + curve_y[int(len(curve_y) / 2)]) / 3
        plt.annotate("Кривая - " + str(i), xy=(xmean, ymean), xycoords='data')
        # Точки для безье
        plt.plot(
            points[:, 0],
            points[:, 1],
            'ro:',
            color='darkblue'
        )
    else:
        plt.plot(
            curve[:, 0],
            curve[:, 1], lw=2.8, color='black'
        )

# Расчет координат кривых линий
def calculate_line_curve(row, x_coord_line, y_coord_line, df_formula, x_shift, y_shift):
    # список всех x и y отклонений кривых линий
    x_deviation = list()
    y_deviation = list()

    try:
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
    except NameError:
        return "error_line"

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

            list_new_x.append(((x_coord_line[i] - x_shift + x_coord_line[i + 1] - x_shift) / 2) * d_x_first + x_shift)
            list_new_y.append(((y_coord_line[i] - y_shift + y_coord_line[i + 1] - y_shift) / 2) * d_y_first + y_shift)

        # если отклонений несколько
        else:
            k = len(x_deviation[j])
            for r in range(1, k + 1):
                d_x_first = x_deviation[j][r - 1]
                d_y_first = y_deviation[j][r - 1]

                # формула расчета координат в отношении
                alpha = r / (k + 1 - r)
                list_new_x.append(((x_coord_line[i] - x_shift + alpha * (x_coord_line[i + 1] - x_shift)) / (1 + alpha)) * d_x_first + x_shift)
                list_new_y.append(((y_coord_line[i] - y_shift + alpha * (y_coord_line[i + 1] - y_shift)) / (1 + alpha)) * d_y_first + y_shift)

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

def add_to_pdf(pdf, x1, x2, y1, y2):
    plt.axis('off')
    plt.xlim([x1, x2])
    plt.ylim([y1, y2])
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    pdf.savefig(bbox_inches='tight')
