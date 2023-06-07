"""
Genres public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, abort, g, request
from marshmallow import ValidationError
from .schema_public import BookRatingSchema
from init_dep import db
from modules.books.model import Book
from .model import BookRating
from datetime import datetime


def post_book_rating():
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
    book = None
    if request.json.get("book_id", None) is not None:
        book = Book.query.filter(Book.id == request.json.get("book_id")).first()

    if book is None:
        print(",..,,")
        abort(400)

    errors = {}

    # validate data
    try:
        data = BookRatingSchema().load(request.json)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        print(errors)
        return jsonify({"error": errors}), 400

    book_rating_exist = BookRating.query.filter(BookRating.user_id == user.id,
                                                BookRating.book_id == book.id).first()

    if book_rating_exist is not None:
        print("aaa")
        abort(400)

    # save book
    book_rating = BookRating(
        book=book,
        user=user,
        rating=data.get("rating"),
        timestamp=datetime.now(),
    )

    new_rating = (
        (book.average_rating * book.ratings_count) + float(data.get("rating"))
    ) / (book.ratings_count + 1)
    book.average_rating = round(new_rating, 2)
    book.ratings_count = book.ratings_count + 1

    db.session.add(book_rating)
    db.session.commit()

    # response
    return jsonify({"book_rating": BookRatingSchema().dump(book_rating)}), 201


def patch_book_rating(book_rating_id):
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    # get book_rating
    book_rating = BookRating.query.filter(BookRating.id == book_rating_id).first()
    if book_rating is None:
        abort(404)

    # save alert
    if "rating" in request.json:
        new_rating = (
            (book_rating.book.average_rating * book_rating.book.ratings_count)
            - float(book_rating.rating)
            + float(request.json.get("rating")) / book_rating.book.ratings_count
        )
        book_rating.book.average_rating = round(new_rating, 2)
        book_rating.rating = float(request.json.get("rating"))

    db.session.commit()

    # response
    return jsonify({"book_rating": BookRatingSchema().dump(book_rating)}), 200
