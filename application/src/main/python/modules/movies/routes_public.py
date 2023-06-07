"""
Movie public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, abort, g

from init_dep import db

from .model import Movie
from .schema_public import MovieSchema
from modules.ratings.model import Rating
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import math


def get_movies(page=1):
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    query = Movie.query.order_by(Movie.id.asc())

    # retrieve and return results
    results = list(query.limit(30).offset((page - 1) * 30))
    if len(results) > 0:
        # prep initial output
        output = {
            "movies": MovieSchema(
                many=True,
                context={
                    "user_id": user.id,
                },
            ).dump(results),
            "total": query.count(),
        }

        return jsonify(output), 200

    return "", 204


def get_movies_recommended():
    
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    user_ratings = Rating.query.filter_by(user_id=user.id).all()

    if len(user_ratings) > 0:
        other_users_ratings = (
            Rating.query.filter(
                Rating.movie_id.in_([rating.movie_id for rating in user_ratings])
            )
            .filter(Rating.user_id != user.id)
            .all()
        )

        if len(other_users_ratings) > 0:
            # Obtener las calificaciones del usuario objetivo en forma de matriz
            user_ratings_matrix = [[rating.rating] for rating in user_ratings]

            # Obtener las calificaciones de los otros usuarios en forma de matriz
            other_users_ratings_matrix = [
                [rating.rating] for rating in other_users_ratings
            ]

            # Calcular la similitud del coseno entre el usuario objetivo y los otros usuarios
            similarity_scores = cosine_similarity(
                user_ratings_matrix, other_users_ratings_matrix
            )

            # Crear un diccionario para almacenar la suma ponderada de las calificaciones
            weighted_ratings = defaultdict(float)

            # Iterar sobre las calificaciones de los otros usuarios
            for i, rating in enumerate(other_users_ratings):
                similarity_score = similarity_scores[0][
                    i
                ]  # Obtener la similitud del coseno para el usuario actual
                for movie_rating in rating.user.ratings:
                    # Calcular la calificación ponderada multiplicando la calificación por la similitud
                    weighted_rating = movie_rating.rating * similarity_score
                    weighted_ratings[movie_rating.movie] += weighted_rating

            recommended_movies = sorted(
                weighted_ratings, key=weighted_ratings.get, reverse=True
            )
            recommended_movies_filter = []

            for movie in recommended_movies:
                is_rating = False
                for rating in movie.ratings:
                    if rating.user_id == user.id:
                        is_rating = True
                if is_rating == False:
                    recommended_movies_filter.append(movie)

            if len(recommended_movies) > 0:
                # prep initial output
                output = {
                    "movies": MovieSchema(
                        many=True,
                        context={
                            "user_id": user.id,
                        },
                    ).dump(recommended_movies_filter[:4]),
                    "total": 5,
                }
                return jsonify(output), 200

    return "", 204


def get_recommended_results():
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)

    user_ratings = Rating.query.filter_by(user_id=user.id).all()

    if len(user_ratings) > 0:
        other_users_ratings = (
            Rating.query.filter(
                Rating.movie_id.in_([rating.movie_id for rating in user_ratings])
            )
            .filter(Rating.user_id != user.id)
            .all()
        )

        if len(other_users_ratings) > 0:
            # Obtener las calificaciones del usuario objetivo en forma de matriz
            user_ratings_matrix = [[rating.rating] for rating in user_ratings]

            # Obtener las calificaciones de los otros usuarios en forma de matriz
            other_users_ratings_matrix = [
                [rating.rating] for rating in other_users_ratings
            ]

            # Calcular la similitud del coseno entre el usuario objetivo y los otros usuarios
            similarity_scores = cosine_similarity(
                user_ratings_matrix, other_users_ratings_matrix
            )

            # Crear un diccionario para almacenar la suma ponderada de las calificaciones
            weighted_ratings = defaultdict(float)

            # Iterar sobre las calificaciones de los otros usuarios
            for i, rating in enumerate(other_users_ratings):
                similarity_score = similarity_scores[0][
                    i
                ]  # Obtener la similitud del coseno para el usuario actual
                for movie_rating in rating.user.ratings:
                    # Calcular la calificación ponderada multiplicando la calificación por la similitud
                    weighted_rating = movie_rating.rating * similarity_score
                    weighted_ratings[movie_rating.movie] += weighted_rating

            recommended_movies = sorted(
                weighted_ratings, key=weighted_ratings.get, reverse=True
            )
            recommended_movies_filter = []

            for movie in recommended_movies:
                is_rating = False
                for rating in movie.ratings:
                    if rating.user_id == user.id:
                        is_rating = True
                if is_rating == False:
                    recommended_movies_filter.append(movie)

            actual_movies = [rating.movie for rating in user_ratings]

            # Calcular el número de recomendaciones relevantes
            recomendaciones_relevantes = [
                movie for movie in recommended_movies if movie in actual_movies
            ]

            # Calcular la precisión dividiendo el número de recomendaciones relevantes entre el número total de recomendaciones
            precision = len(recomendaciones_relevantes) / len(recommended_movies)

            # Calcular el número total de elementos relevantes
            total_relevantes = len(actual_movies)

            # Calcular el Recall dividiendo el número de recomendaciones relevantes entre el número total de elementos relevantes
            recall = len(recomendaciones_relevantes) / total_relevantes

            # Crear una lista de relevancia para las películas recomendadas
            relevancia_recomendadas = [
                1 if movie in actual_movies else 0 for movie in recommended_movies
            ]

            # Calcular el NDCG
            dcg = 0.0
            idcg = 0.0
            for i, relevancia in enumerate(relevancia_recomendadas):
                dcg += (2**relevancia - 1) / (
                    math.log2(i + 2)
                )  # Discounted Cumulative Gain
                idcg += (2**1 - 1) / (
                    math.log2(i + 2)
                )  # Ideal Discounted Cumulative Gain

            ndcg = dcg / idcg  # Normalized Discounted Cumulative Gain

            if len(recommended_movies) > 0:
                # prep initial output
                output = {
                    "NDCG": ndcg,
                    "recall": recall,
                    "Precisión": precision,
                }
                return jsonify(output), 200
