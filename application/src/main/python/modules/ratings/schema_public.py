"""
Schemas to serialize/deserialize/validate models for the Rating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields

from init_dep import ma
from .model import Rating

class RatingSchema(ma.Schema):
    """Public schema for Rating model"""

    class Meta:
        """RatingSchema meta data"""

        model = Rating

        # fields to expose
        fields = ('id', 'rating', 'timestamp', 'user', 'movie', 'movie_id', 'user_id')
        dump_only = ['id']

    # nested schema
    user = fields.Nested(
        'UserSchema',
        only=('id', 'username'))

    # nested schema
    movie = fields.Nested(
        'MovieSchema',
        only=('id', 'title'))
    
    id = fields.UUID()
    movie_id = fields.Integer(required=True)
    rating = fields.Float(required=True)
    
