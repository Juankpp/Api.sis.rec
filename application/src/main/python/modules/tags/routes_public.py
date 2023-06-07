"""
Genres public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime

from flask import jsonify, g, abort, request
from marshmallow import ValidationError

from init_dep import db

from .schema_public import TagSchema
from modules.movies.model import Movie
from .model import Tag


def get_tags():
    """Performs a basic system health check/smoke test.

    :returns: JSON string; status code
    :rtype: (str, int)
    """
    return jsonify({"success": True}), 200


def post_tag():
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    movie = None
    if request.json.get("movie_id", None) is not None:
        movie = Movie.query.filter(Movie.id == request.json.get("movie_id")).first()

    if movie is None:
        abort(401)

    errors = {}

    # validate data
    try:
        data = TagSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    # save tag
    tag = Tag(
        movie=movie,
        user=user,
        tag=data.get("tag"),
        timestamp=datetime.now(),
    )
    db.session.add(tag)
    db.session.commit()

    # response
    return jsonify({"tag": TagSchema().dump(tag)}), 201
