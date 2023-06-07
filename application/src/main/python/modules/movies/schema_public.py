"""
Schemas to serialize/deserialize/validate models for the Movie module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""


from init_dep import ma
from .model import Movie
from marshmallow import fields, pre_dump

class MovieSchema(ma.Schema):
    """Public schema for Movie model"""

    class Meta:
        """MovieSchema meta data"""

        model = Movie

        # fields to expose
        fields = ('id', 'title', 'year', 'genres', 'tags', 'ratings')

    genres = fields.Nested(
        'GenreSchema',
        only=('id', 'genre'),
        many=True)

    tags = fields.Nested(
        'TagSchema',
        only=('id', 'tag'),
        many=True)

    ratings = fields.Nested(
        'RatingSchema',
        only=('id', 'rating', 'movie_id', 'user_id'),
        many=True)

    @pre_dump
    def rating_filter(self, data, **kwargs):
        if self.context and self.context.get('user_id'):
            filter_rating = []
            for rating in data.ratings:
                if rating.user_id == self.context.get('user_id'):
                    filter_rating.append(rating)
            data.ratings = filter_rating
        
        return data

