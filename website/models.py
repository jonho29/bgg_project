from . import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), unique = True)
    rank = db.Column(db.String(10))
    rating = db.Column(db.String(10))
    player_count = db.Column(db.String(10))
    suggested_numplayers = db.Column(db.JSON)
    categories = db.Column(db.JSON)
    mechanics = db.Column(db.JSON)
