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

@app.route('/game/', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        # Check if publisher exists
        q = db.session.query(Publisher).filter(Publisher.id == request.json['publisher_id'])
        if db.session.query(q.exists()).scalar():
            publisher = Publisher.query.get(request.json['publisher_id'])
        else:
            return 'Publisher {} doesn\'t exist'.format(request.json['publisher_id']), 400
        # Check if genre(s) exists
        genres = []
        for genre_id in request.json['genre_id']:
            q = db.session.query(Genre).filter(Genre.id == genre_id)
            if db.session.query(q.exists()).scalar():
                genre = Genre.query.get(genre_id)
                genres.append(genre)

        game = Game(request.json['title'].capitalize(), request.json['release'], publisher)
        for genre in genres:
            game.genres.append(genre)

        db.session.add(game)
        db.session.commit()

        return 'Game {} has been added with ID: {}'.format(game.title, game.id), 201
    games = Game.query.all()
    games_schema = GameSchema(many=True)
    return jsonify(games_schema.dump(games))

@app.route('/game/<int:id>')
def game_details(id):
    game = Game.query.get(id)
    game_schema = GameSchema()
    return game_schema.dump(game)

@app.route('/publisher/', methods=['GET', 'POST'])
def publisher():
    if request.method == 'POST':
        q = db.session.query(Publisher).filter(Publisher.name == request.json['name'].capitalize())
        if db.session.query(q.exists()).scalar():
            return 'Publisher exists already.', 400
        publisher = Publisher(request.json['name'].capitalize())
        db.session.add(publisher)
        db.session.commit()
        return 'Publisher {} has been added with ID {}'.format(publisher.name, publisher.id), 201
    publishers = Publisher.query.all()
    pubs_schema = PublisherSchema(many=True)
    return jsonify(pubs_schema.dump(publishers))

@app.route('/publisher/<int:id>')
def publisher_detail(id):
    publisher = Publisher.query.get(id)
    pub_schema = PublisherSchema()
    return pub_schema.dump(publisher)

@app.route('/genre/', methods=['GET', 'POST'])
def genre():
    if request.method == 'POST':
        q = db.session.query(Genre).filter(Genre.name == request.json['name'].capitalize())
        if db.session.query(q.exists()).scalar():
            return 'Genre exists already.', 400
        genre = Genre(request.json['name'].capitalize())
        db.session.add(genre)
        db.session.commit()
        return 'Genre {} has been added with ID {}'.format(genre.name, genre.id), 201
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
