import math
import matplotlib.pyplot as plt
import numpy as np
from models.model_general import get_detail_name
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


def add_to_pdf(pdf, x1, x2, y1, y2):
    plt.axis('off')
    plt.xlim([x1, x2])
    plt.ylim([y1, y2])
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    pdf.savefig(bbox_inches='tight')
