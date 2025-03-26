from flask import Blueprint, render_template

saved = Blueprint('saved', __name__)

@saved.route('/saved')
def stored_games():
    return render_template('saved.html')