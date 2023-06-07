"""
Genres public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, abort, g, request
from marshmallow import ValidationError
from .schema_public import SongRatingSchema
from init_dep import db
from modules.songs.model import Song
from .model import SongRating
from datetime import datetime


def post_song_rating():
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    song = None
    if request.json.get("song_id", None) is not None:
        song = Song.query.filter(Song.id == request.json.get("song_id")).first()

    if song is None:
        abort(400)

    errors = {}

    # validate data
    try:
        data = SongRatingSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400
    
    song_rating_exist = SongRating.query.filter(SongRating.user_id == user.id,
                                                SongRating.song_id == song.id).first()

    if song_rating_exist is not None:
        abort(400)

    # save song
    song_rating = SongRating(
        song=song,
        user=user,
        rating=data.get("rating"),
        timestamp=datetime.now(),
    )

    db.session.add(song_rating)
    db.session.commit()

    # response
    return jsonify({"song_rating": SongRatingSchema().dump(song_rating)}), 201


def patch_song_rating(song_rating_id):
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
    print(song_rating_id)
    # get song_rating
    song_rating = SongRating.query.filter(SongRating.id == song_rating_id).first()
    print(song_rating)
    if song_rating is None:
        abort(404)

    # save alert
    if "rating" in request.json:
        song_rating.rating = float(request.json.get("rating"))

    db.session.commit()

    # response
    return jsonify({"song_rating": SongRatingSchema().dump(song_rating)}), 200
