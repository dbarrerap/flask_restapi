from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from models import *
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/')
def game():
    games = Game.query.all()
    games_schema = GameSchema(many=True)
    return jsonify(games_schema.dump(games))

@app.route('/game/<int:id>')
def game_details(id):
    game = Game.query.get(id)
    game_schema = GameSchema()
    return game_schema.dump(game)

@app.route('/publisher/')
def publisher():
    publishers = Publisher.query.all()
    pubs_schema = PublisherSchema(many=True)
    return jsonify(pubs_schema.dump(publishers))

@app.route('/publisher/<int:id>')
def publisher_detail(id):
    publisher = Publisher.query.get(id)
    pub_schema = PublisherSchema()
    return pub_schema.dump(publisher)

@app.route('/genre/')
def genre():
    genres = Genre.query.all()
    genres_schema = GenreSchema(many=True)
    return jsonify(genres_schema.dump(genres))

@app.route('/genre/<int:id>')
def genre_details(id):
    genre = Genre.query.get(id)
    genre_schema = GenreSchema()
    return genre_schema.dump(genre)


# Main
if __name__ == '__main__':
    app.run(debug=True)
