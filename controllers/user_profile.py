from app import app
from flask import render_template


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():

    html = render_template(
        'user_profile.html'
    )

    return html