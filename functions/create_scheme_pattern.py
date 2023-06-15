from functions.create_scheme import *

def create_user_scheme_pattern(conn, user_param, list_id_detail, name_pattern, func_name):
    # создание словаря формул
    df_formula = pd.DataFrame()
    for id_detail in list_id_detail:
        df_formula = pd.concat([df_formula, get_formula_detail(conn, id_detail)], axis=0, ignore_index=True)

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
    df_line = pd.DataFrame()

    for id_detail in list_id_detail:
        df_line = pd.concat([df_line, get_line_detail(conn, id_detail)], axis=0, ignore_index=True)

    x_coord_line_straight = []
    y_coord_line_straight = []
    line_curve = []
    line_curve_points = []

    # Список всех координат линий
    x_list = []
    y_list = []

    # Список координат линий для разных уровней деталей
    x_list_coord_max = list()
    y_list_coord_max = list()

    # Подсчет максимального значения координат для разных уровней деталей
    x_detail_max = 0
    y_detail_max = 0

    # Итоговое значение сдвига координат
    x_shift = 0
    y_shift = 0

    id_detail_one = df_line.loc[0, "detail_id"]
    count_detail = 1

    # Максимальное значение сдвига координат
    x_shift_max = 0

    # Расчёт координат линий
    for index, row in df_line.iterrows():
        id_detail = row["detail_id"]
        if id_detail != id_detail_one:
            id_detail_one = id_detail
            count_detail += 1
            x_shift = x_detail_max

        if count_detail == 3:
            if x_shift_max > x_shift:
                count_detail -= 1
            else:
                count_detail = 1
                y_shift = y_detail_max
                if x_shift > x_shift_max:
                    x_shift_max = x_shift
                x_shift = 0
                x_list_coord_max.clear()

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

        x_coord_line.append(x1 + x_shift)
        y_coord_line.append(y1 + y_shift)
        x_coord_line.append(x2 + x_shift)
        y_coord_line.append(y2 + y_shift)

        x_list_coord_max.append(x1 + x_shift)
        y_list_coord_max.append(y1 + y_shift)
        x_list_coord_max.append(x2 + x_shift)
        y_list_coord_max.append(y2 + y_shift)

        if df_line.loc[index, 'x_deviation'] == '':
            x_coord_line_straight.append(x_coord_line)
            y_coord_line_straight.append(y_coord_line)
        else:
            try:
                curve, points_curve = calculate_line_curve(row, x_coord_line, y_coord_line, df_formula, x_shift, y_shift)
            except ValueError:
                return "error_line"

            line_curve.append(curve)
            line_curve_points.append(points_curve)
            for coord in curve:
                x_list.append(coord[0])
                y_list.append(coord[1])

        x_list += x_coord_line
        y_list += y_coord_line

        x_detail_max = max(x_list_coord_max) - 1
        y_detail_max = max(y_list_coord_max) - 1

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

    name_scheme_pattern = 'static/pdf/' + str(name_pattern) + '.pdf'
    pdf = PdfPages(name_scheme_pattern)

    for i in range(pages_y):
        y = 1 + 29.7 * i
        for j in range(pages_x):
            x = 1 + 21 * j
            plt.title("Строка " + str(i + 1) +
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

    name = 'static/image/save_patterns/' + str(name_pattern) + '.jpg'
    plt.savefig(name, bbox_inches='tight')
    pdf.close()

    return name

def add_to_pdf(pdf, x1, x2, y1, y2):
    plt.axis('off')
    plt.xlim([x1, x2])
    plt.ylim([y1, y2])
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    pdf.savefig(bbox_inches='tight')