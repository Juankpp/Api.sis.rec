"""
Schemas to serialize/deserialize/validate models for the Song module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields, pre_dump

from init_dep import ma
from .model import Song

class SongSchema(ma.Schema):
    """Public schema for Song model"""

    class Meta:
        """SongSchema meta data"""

        model = Song

        # fields to expose
        fields = ('id', 'song', 'link', 'text', 'artist', 'ratings')

    # nested schema
    artist = fields.Nested(
        'ArtistSchema',
        only=('id', 'name'))

    ratings = fields.Nested(
        'SongRatingSchema',
        only=('id', 'rating', 'song_id', 'user_id'),
        many=True)

    @pre_dump
    def rating_filter(self, data, **kwargs):
        if self.context and self.context.get('user_id'):
            filter_rating = []
            for song_rating in data.ratings:
                if song_rating.user_id == self.context.get('user_id'):
                    filter_rating.append(song_rating)
            data.ratings = filter_rating
        return data