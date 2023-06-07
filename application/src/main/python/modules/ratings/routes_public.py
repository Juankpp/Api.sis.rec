"""
Genres public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, abort, g, request
from marshmallow import ValidationError
from .schema_public import RatingSchema
from init_dep import db
from modules.movies.model import Movie
from .model import Rating
from datetime import datetime

def post_rating():
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
        
    movie = None
    if request.json.get("movie_id", None) is not None:
        movie = Movie.query.filter(Movie.id == request.json.get("movie_id")).first()

    if movie is None:
        abort(400)

    errors = {}

    # validate data
    try:
        data = RatingSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    rating_exist = Rating.query.filter(Rating.user_id == user.id,
                                                Rating.movie_id == movie.id).first()

    if rating_exist is not None:
        abort(400)

    # save rating
    rating = Rating(
        movie=movie,
        user=user,
        rating=data.get("rating"),
        timestamp=datetime.now(),
    )
 
    db.session.add(rating)
    db.session.commit()

    # response
    return jsonify({"rating": RatingSchema().dump(rating)}), 201


def patch_rating(rating_id):
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    # get rating
    rating = Rating.query.filter(Rating.id == rating_id).first()
    if rating is None:
        abort(404)

    # save alert
    if "rating" in request.json:
        rating.rating = float(request.json.get("rating"))

    db.session.commit()

    # response
    return jsonify({"rating": RatingSchema().dump(rating)}), 200
