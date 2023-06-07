"""
Schemas to serialize/deserialize/validate models for the SongRating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields

from init_dep import ma
from .model import SongRating

class SongRatingSchema(ma.Schema):
    """Public schema for SongRating model"""

    class Meta:
        """SongRatingSchema meta data"""

        model = SongRating

        # fields to expose
        fields = ('id', 'rating', 'timestamp', 'user', 'song', 'song_id', 'user_id')
        dump_only = ['id']

    # nested schema
    user = fields.Nested(
        'UserSchema',
        only=('id', 'username'))

    # nested schema
    song = fields.Nested(
        'SongSchema',
        only=('id', 'song', 'link', 'text', 'artist', 'ratings'))
    
    id = fields.UUID()
    song_id = fields.UUID(required=True)
    rating = fields.Float(required=True)
    
