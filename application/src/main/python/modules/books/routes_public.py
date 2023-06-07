"""
Genres public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, g, abort, request
from marshmallow import ValidationError

from .model import Book
from .schema_public import BookSchema
from .model import Book
from init_dep import db
from modules.book_ratings.model import BookRating

from flask import jsonify, abort, g

from init_dep import db

from .model import Book
from .schema_public import BookSchema
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import math



def get_books(page=1):
    
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
    
    query = Book.query.order_by(Book.id.asc())
    
    # retrieve and return results
    results = list(query.limit(30).offset((page - 1) * 30))
    if len(results) > 0:
        # prep initial output
        output = {
            'books': BookSchema(many=True, context={
                    'user_id': user.id,
                }).dump(results),
            'total': query.count()
        }
        return jsonify(output), 200

    return '', 204 

def patch_book(book_id):
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    # get book
    book = Book.query.filter(Book.id == book_id).first()
    if book is None:
        abort(404)

    if "text_review" in request.json:
        book.text_reviews_count = book.text_reviews_count + 1

    db.session.commit()

    # response
    return jsonify({"book": BookSchema().dump(book)}), 200

def get_books_recommended():
    
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
    
    user_ratings = BookRating.query.filter_by(user_id=user.id).all()

    if len(user_ratings) > 0:
    
        other_users_ratings = BookRating.query \
            .filter(BookRating.book_id.in_([rating.book_id for rating in user_ratings])) \
            .filter(BookRating.user_id != user.id) \
            .all() \
        
        if len(other_users_ratings) > 0:
        
            # Obtener las calificaciones del usuario objetivo en forma de matriz
            user_ratings_matrix = [[rating.rating] for rating in user_ratings]

            # Obtener las calificaciones de los otros usuarios en forma de matriz
            other_users_ratings_matrix = [[rating.rating] for rating in other_users_ratings]

            # Calcular la similitud del coseno entre el usuario objetivo y los otros usuarios
            similarity_scores = cosine_similarity(user_ratings_matrix, other_users_ratings_matrix)

            # Crear un diccionario para almacenar la suma ponderada de las calificaciones        
            weighted_ratings = defaultdict(float)

            # Iterar sobre las calificaciones de los otros usuarios
            for i, rating in enumerate(other_users_ratings):
                similarity_score = similarity_scores[0][i]  # Obtener la similitud del coseno para el usuario actual
                for book_rating in rating.user.book_ratings:

                    # Calcular la calificación ponderada multiplicando la calificación por la similitud
                    weighted_rating = book_rating.rating * similarity_score
                    weighted_ratings[book_rating.book] += weighted_rating

            recommended_books = sorted(weighted_ratings, key=weighted_ratings.get, reverse=True)
            recommended_books_filter = []
            
            for book in recommended_books:
                is_rating = False
                for rating in book.ratings:
                    if rating.user_id == user.id:
                        is_rating = True
                if is_rating == False:
                    recommended_books_filter.append(book)
            
            if len(recommended_books) > 0:
                # prep initial output
                output = {
                    'books': BookSchema(many=True, context={
                            'user_id': user.id,
                        }).dump(recommended_books_filter[:4]),
                    'total': 5
                }
                return jsonify(output), 200
    return "", 204
    
