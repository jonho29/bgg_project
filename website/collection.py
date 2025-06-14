from flask import Blueprint, render_template, Response
from .models import Game

collection = Blueprint('collection', __name__)

@collection.route('/collection')
def stored_games() -> Response:
    games = Game.query.all()
    return render_template('collection.html', games = games)