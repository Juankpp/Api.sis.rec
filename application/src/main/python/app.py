"""
Application generator.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Flask
from flask_cors import CORS

from init_dep import db, ma

from modules import tags, ratings, users, genres, movies, \
    artists, songs, authors, books, book_ratings, song_ratings


def create_app(config):
    """Initializes the public application Flask object.

    :param config: Configuration ADT
    :type config: Config
    :returns: Flask app object
    """

    # init app
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app, resources={r"/*": {"origins": "*"}})

    # init database
    db.init_app(app)

    # init Marshmallow
    ma.init_app(app)

    # register modules
    movies.register(app)    
    users.register(app)
    ratings.register(app)
    tags.register(app)
    genres.register(app)
    artists.register(app)
    songs.register(app)
    authors.register(app)
    books.register(app)
    book_ratings.register(app)
    song_ratings.register(app)

    return app
