from app import app
from flask import render_template
# from utils import get_db_connection


@app.route('/', methods=['get', 'post'])
def search():
    # conn = get_db_connection()
    html = render_template(
        'search.html'
    )
    return html
