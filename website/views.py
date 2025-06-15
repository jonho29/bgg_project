from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response
from .bgg.bgg import search_via_name, search_via_id
from .models import Game
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
def home() -> Response:
    if request.method == 'POST':
        searched_name = request.form.get('game')
        retrieved_games = search_via_name(searched_name)
        return render_template('retrieved_games.html', searched_for = searched_name, retrieved_games = retrieved_games)
    return render_template('home.html')

@views.route('/id/<game_id>', methods = ['GET', 'POST'])
def game(game_id: str) -> Response | str:
    if game_id.isdigit():
        retrieved_game = search_via_id(int(game_id))
        if not all(retrieved_game.values()):
            return render_template('error.html', error_message = f'The object with ID: {game_id} is not listed as a board game on BGG')
        if request.method == 'POST':
            name = retrieved_game['name']
            rank = int(retrieved_game['rank'])
            rating = float(retrieved_game['rating'])
            player_count = retrieved_game['player_count']
            suggested_numplayers = retrieved_game['suggested_numplayers']
            categories = retrieved_game['categories']
            mechanics = retrieved_game['mechanics']

            # Check if game exists first
            game = db.session.query(Game.id).filter(Game.name == name)
            if db.session.query(game.exists()).scalar():
                return render_template('error.html', error_message = 'Game already exists in collection')
            new_game = Game(id = game_id, 
                            name = name, 
                            rank = rank,
                            rating = rating,
                            player_count = player_count, 
                            suggested_numplayers = suggested_numplayers, 
                            categories = categories, 
                            mechanics = mechanics)
            db.session.add(new_game)
            db.session.commit()

            return redirect(url_for('collection.stored_games'))
        return render_template('single_game.html', game_id = game_id, retrieved_game = retrieved_game)
    else:
        return render_template('error.html', error_message = 'Invalid game ID')

@views.route('/delete-game', methods = ['POST'])
def delete_game() -> Response:
    game = json.loads(request.data)
    game_id = game['gameId']
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return jsonify({})