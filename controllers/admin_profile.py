from app import app
from flask import render_template, request, session, make_response

@app.route('/admin_profile', methods=['GET', 'POST'])
def admin_profile():

    html = render_template(
        'admin_profile.html'
    )

    return html