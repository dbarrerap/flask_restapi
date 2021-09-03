from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Models
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    games = db.relationship('Game', backref='genre')

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    releases = db.relationship('Game', backref='publisher')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    release = db.Column(db.DateTime)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)

# Marshmallow Schema
class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        include_relationships = True

class PublisherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Publisher
        include_relationships = True

class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        include_fk = True


# Routes
@app.route('/')
def index():
    return '<h1>Games API</h1>'


# Main
if __name__ == '__main__':
    app.run(debug=True)
