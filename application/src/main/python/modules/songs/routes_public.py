"""
Song public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, g, abort
from .model import Song
from .schema_public import SongSchema
from .model import Song

from modules.song_ratings.model import SongRating
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import math
from sklearn.feature_extraction.text import TfidfVectorizer


def get_songs(page=1):
    
    query = Song.query.order_by(Song.id.asc())
    
    # retrieve and return results
    results = list(query.limit(30).offset((page - 1) * 30))
    if len(results) > 0:

        # prep initial output
        output = {
            'songs': SongSchema(many=True).dump(results),
            'total': query.count()
        }

        return jsonify(output), 200

    return '', 204


def get_songs_recommended():
    
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
    
    user_ratings = SongRating.query.filter_by(user_id=user.id).all()

    if len(user_ratings) > 0:
    
        other_users_ratings = (
            SongRating.query
            .filter(SongRating.song_id.in_([rating.song_id for rating in user_ratings]))
            .filter(SongRating.user_id != user.id)
            .all()
        )
        
        if len(other_users_ratings) > 0:
        
            # Obtener las calificaciones del usuario objetivo en forma de matriz
            user_ratings_matrix = [[rating.rating] for rating in user_ratings]

            # Obtener las calificaciones de los otros usuarios en forma de matriz
            other_users_ratings_matrix = [[rating.rating] for rating in other_users_ratings]

            # Calcular la similitud del coseno entre el usuario objetivo y los otros usuarios
            similarity_scores = cosine_similarity(user_ratings_matrix, other_users_ratings_matrix)

            # Crear un diccionario para almacenar la suma ponderada de las calificaciones
            weighted_ratings = defaultdict(float)
            
            weighted_ratings = defaultdict(float)

            # Iterar sobre las calificaciones de los otros usuarios
            for i, rating in enumerate(other_users_ratings):
                similarity_score = similarity_scores[0][i]  # Obtener la similitud del coseno para el usuario actual
                for song_rating in rating.user.ratings:
                    # Calcular la calificación ponderada multiplicando la calificación por la similitud
                    weighted_rating = song_rating.rating * similarity_score
                    weighted_ratings[song_rating.song] += weighted_rating

            recommended_songs = sorted(weighted_ratings, key=weighted_ratings.get, reverse=True)
            recommended_songs_filter = []
            
            for song in recommended_songs:
                is_rating = False
                for rating in song.ratings:
                    if rating.user_id == user.id:
                        is_rating = True
                if is_rating == False:
                    recommended_songs_filter.append(song)
            
            if len(recommended_songs) > 0:
                # prep initial output
                output = {
                    'songs': SongSchema(many=True, context={
                            'user_id': user.id,
                        }).dump(recommended_songs_filter[:4]),
                    'total': 5
                }
                return jsonify(output), 200

    return "", 204
    
def get_songs_recommended_based_content():
    
    # get user & perform sanity check
    user = g.user
    if user is None:
        abort(500)
        
    # Realizar la consulta para obtener las canciones de referencia
    song_ratings = SongRating.query.filter(SongRating.user_id == user.id).all()

    ids = [song_rating.song_id for song_rating in song_ratings]

    reference_songs = Song.query.filter(Song.id.in_(ids)).all()

    # Obtener las letras de las canciones de referencia
    reference_lyrics = [song.text for song in reference_songs]

    # Obtener todas las canciones de la base de datos
    all_songs = Song.query.all()

    # Obtener las letras de todas las canciones
    all_lyrics = [song.text for song in all_songs]

    # Preprocesamiento de texto y representación vectorial
    vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
    reference_vectors = vectorizer.fit_transform(reference_lyrics)
    all_vectors = vectorizer.transform(all_lyrics)

    for reference_index, reference_song in enumerate(reference_songs):
        # Cálculo de similitud entre la canción de referencia y todas las demás canciones
        similarity_scores = cosine_similarity(reference_vectors[reference_index], all_vectors)

        # Obtener las canciones más similares
        similar_songs_indices = similarity_scores.argsort()[0][::-1][1:]

        # Imprimir las canciones más similares
        print(f"Canciones similares a la canción de referencia {reference_song.song}:")
        ids_recommended = []
        for index in similar_songs_indices:
            similar_song = all_songs[index]
            ids_recommended.append(similar_song.id)
        
        song_recommend = Song.query.filter(Song.id.in_(ids_recommended)).all() 
        
        if len(similar_songs_indices) > 0:
            # prep initial output
            output = {
                'songs': SongSchema(many=True).dump(song_recommend[:4]),
                'total': 5
            }
            return jsonify(output), 200    
        
    return "", 204