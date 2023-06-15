from models.model_general import get_detail_name
from functions.create_scheme import *


def create_user_scheme_detail(conn, user_param, id_detail, pdf, func_name):
    # создание словаря формул
    df_formula = get_formula_detail(conn, id_detail)
    df_formula = df_formula.set_index('formula_name').T.to_dict('list')

    measurements = dict(zip(user_param["Обозначение"], user_param["Значение"]))
    for key in measurements:
        if measurements[key] != '':
            measurements[key] = float(measurements[key])

    measurements['Корень'] = math.sqrt
    measurements['Степень'] = math.pow

    try:
        # расчёт всех формул в зависимости от значений мерок
        for formula in df_formula:
            df_formula[formula] = eval(df_formula[formula][0], {}, measurements)
    except NameError:
        return "error_mes"

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

        try:
            x1 = eval(f"{row['x_first_coord']}", measurements, df_formula)
            y1 = eval(f"{row['y_first_coord']}", measurements, df_formula)

            x2 = eval(f"{row['x_second_coord']}", measurements, df_formula)
            y2 = eval(f"{row['y_second_coord']}", measurements, df_formula)
        except Exception:
            return "error_form"

        x_coord_line.append(x1)
        y_coord_line.append(y1)
        x_coord_line.append(x2)
        y_coord_line.append(y2)

        if df_line.loc[index, 'x_deviation'] == '':
            x_coord_line_straight.append(x_coord_line)
            y_coord_line_straight.append(y_coord_line)
        else:
            try:
                curve, points_curve = calculate_line_curve(row, x_coord_line, y_coord_line, df_formula, 0, 0)
            except ValueError:
                return "error_line"
            line_curve.append(curve)
            line_curve_points.append(points_curve)
            for coord in curve:
                x_list.append(coord[0])
                y_list.append(coord[1])

        x_list += x_coord_line
        y_list += y_coord_line

    try:
        length_x = max(x_list) - min(x_list)
        length_y = max(y_list) - min(y_list)
    except ValueError:
        return "error_line"

    # Определение масштаба схемы
    if length_x >= length_y:
        setting_plt(length_x + 2)
    else:
        setting_plt(length_y + 2)

    if func_name != "admin":
        plt.axis('off')

    # количество листов по иксу
    pages_x = math.ceil(length_x / 21)
    # количество листов по игреку
    pages_y = math.ceil(length_y / 29.7)

    if pages_x == 1 and pages_y == 1:
        plt.figure(figsize=((1.8 + (pages_x + 1) * 21) / 2.54, (1.8 + (pages_y + 1) * 29.7) / 2.54))
    elif pages_x == 1 and pages_y != 1:
        plt.figure(figsize=((1.8 + (pages_x + 1) * 21) / 2.54, (1 + pages_y * 29.7) / 2.54))
    elif pages_x != 1 and pages_y == 1:
        plt.figure(figsize=((1 + pages_x * 21) / 2.54, (1.8 + (pages_y + 1) * 29.7) / 2.54))
    else:
        plt.figure(figsize=((1 + pages_x * 21) / 2.54, (1 + pages_y * 29.7) / 2.54))

    i = 0
    # Построение всех линий
    for x_straight, y_straight in zip(x_coord_line_straight, y_coord_line_straight):
        i = i + 1
        build_line_straight(x_straight, y_straight, func_name, i)
    i = 0
    for curves, curves_points in zip(line_curve, line_curve_points):
        i = i + 1
        build_line_curve(curves, curves_points, func_name, i)

    for i in range(pages_y):
        y = 1 + 29.7 * i
        for j in range(pages_x):
            x = 1 + 21 * j
            plt.title("Деталь: " + str(get_detail_name(conn, id_detail)) +
                      ". Строка " + str(i + 1) +
                      "; столбец " + str(j + 1),
                      fontsize=29, weight='ultralight', alpha=0.5)
            add_to_pdf(pdf, x, x + 21, y, y + 29.7)

    plt.figure(figsize=(length_x / 2.54, length_y / 2.54))
    plt.xlim([0, length_x + 2])
    plt.ylim([0, length_y + 2])
    i = 0
    for x_straight, y_straight in zip(x_coord_line_straight, y_coord_line_straight):
        i = i + 1
        build_line_straight(x_straight, y_straight, func_name, i)
    i = 0
    for curves, curves_points in zip(line_curve, line_curve_points):
        i = i + 1
        build_line_curve(curves, curves_points, func_name, i)

    if func_name != "admin":
        plt.axis('off')
    else:
        plt.grid(linestyle='--')

    name = 'static/image/save_details/' + str(get_detail_name(conn, id_detail)) + '.jpg'
    plt.savefig(name, bbox_inches='tight')
