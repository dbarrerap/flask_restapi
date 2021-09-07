# Move models here
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import backref

db = SQLAlchemy()
ma = Marshmallow()

# Models
game_genre = db.Table(
    'game_genre',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __init__(self, name):
        self.name = name

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    release = db.Column(db.String)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    publisher = db.relationship('Publisher', backref='releases')
    genres = db.relationship('Genre', secondary=game_genre, backref=db.backref('games'))

    def __init__(self, title, release, publisher):
        self.title = title
        self.release = release
        self.publisher = publisher

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
        # include_fk = True
        # include_relationships = True
    genres = ma.List(ma.HyperlinkRelated('genre'))
    publisher = ma.HyperlinkRelated('publisher')


