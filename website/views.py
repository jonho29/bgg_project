from flask import Blueprint, render_template, request
from .app.bgg import search_via_name, search_via_id

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        searched_name = request.form.get('game')
        retrieved_games = search_via_name(searched_name)
        return render_template('retrieved_games.html', searched_for = searched_name, retrieved_games = retrieved_games)
    return render_template('home.html')

@views.route('/id/<game_id>')
def game(game_id):
    if game_id.isdigit():
        retrieved_game = search_via_id(game_id)
        return render_template('single_game.html', game_id = game_id, retrieved_game = retrieved_game)
    else:
        return 'Invalid game ID'