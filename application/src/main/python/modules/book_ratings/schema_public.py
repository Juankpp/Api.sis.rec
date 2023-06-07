"""
Schemas to serialize/deserialize/validate models for the BookRating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields

from init_dep import ma
from .model import BookRating

class BookRatingSchema(ma.Schema):
    """Public schema for BookRating model"""

    class Meta:
        """BookRatingSchema meta data"""

        model = BookRating

        # fields to expose
        fields = ('id', 'rating', 'timestamp', 'user', 'book', 'book_id', 'user_id')
        dump_only = ['id',]

    # nested schema
    user = fields.Nested(
        'UserSchema',
        only=('id', 'username'))

    # nested schema
    book = fields.Nested(
        'BookSchema',
        only=('id', 'title'))
    
    id = fields.UUID()
    book_id = fields.Integer(required=True)
    rating = fields.Float(required=True)
    
