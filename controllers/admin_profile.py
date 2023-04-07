from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.admin_profile_model import *
import matplotlib.pyplot as plt

@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():
    conn = get_db_connection()
    # переменная для проверки нажатия кнопок
    checked_value = False
    # отвечает за то, какая вкладка на панели администратора открыта
    admin_panel_button = None

    df_formula = get_formula(conn)
    df_line = get_line(conn)
    df_formula = df_formula.set_index('formula_name').T.to_dict('list')
    dlina_izd = 80
    obhvat_bed_1 = 120
    vusota_bed = 40
    obhvat_t = 82

    for formula in df_formula:
        df_formula[formula] = eval(eval(formula, {}, df_formula)[0])

    dots1 = list()
    dots2 = list()
    design = list()
    for i, row in df_line.iterrows():
        x1 = f"{row['x_first_coord']}"
        x2 = f"{row['x_second_coord']}"
        y1 = f"{row['y_first_coord']}"
        y2 = f"{row['y_second_coord']}"
        line_design = f"{row['line_design']}"
        x1 = eval(x1, {}, df_formula)
        y1 = eval(y1, {}, df_formula)
        x2 = eval(x2, {}, df_formula)
        y2 = eval(y2, {}, df_formula)
        dots1.append(x1)
        dots2.append(y1)
        dots1.append(x2)
        dots2.append(y2)
        design.append(line_design)

    for x in range(0, len(dots1)-1, 2):
        if (design[int(x/2)] == "normal"):
            plt.plot([dots1[x], dots1[x + 1]], [dots2[x], dots2[x + 1]], c='black', lw=0.8)
        else:
            plt.plot([dots1[x], dots1[x + 1]], [dots2[x], dots2[x + 1]], c='black', ls='-.', lw=0.8)


    plt.xlim([0, dlina_izd])
    plt.ylim([0, dlina_izd+5])
    plt.savefig("pict.jpg")

    if request.values.get('panel'):
        admin_panel_button = request.values.get('panel').title()

    if request.values.get('add_category'):
        add_category(conn, request.values.get('new_category'))
        admin_panel_button = "Категории"

    elif request.values.get('delete_category'):
        category_id = int(request.values.get('delete_category'))
        admin_panel_button = "Категории"
        delete_category(conn, category_id)

    elif request.values.get('is_edit_category'):
        checked_value = True
        admin_panel_button = "Категории"

    elif request.values.get('edit_category'):
        category_id = int(request.values.get('edit_category'))
        category_name = request.values.get('edit_category_name')
        checked_value = False
        admin_panel_button = "Категории"
        update_category(conn, category_id, category_name)

    df_category = get_category(conn)
    html = render_template(
        'admin_profile.html',
        user_role=session['user_role'],
        admin_panel_button=admin_panel_button,
        category=df_category,
        checked_value=checked_value,
        len=len
    )

    return html
