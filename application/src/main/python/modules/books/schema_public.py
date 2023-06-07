"""
Schemas to serialize/deserialize/validate models for the Book module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields, pre_dump

from init_dep import ma
from .model import Book

class BookSchema(ma.Schema):
    """Public schema for Book model"""

    class Meta:
        """BookSchema meta data"""

        model = Book

        # fields to expose
        fields = ('id', 'title', 'average_rating', 'ratings_count',
                  'text_reviews_count', 'publisher', 'author', 'ratings')

    # nested schema
    author = fields.Nested(
        'AuthorSchema',
        only=('id', 'name'))
    
    ratings = fields.Nested(
        'BookRatingSchema',
        only=('id', 'rating', 'book_id', 'user_id'),
        many=True)
    
    @pre_dump
    def rating_filter(self, data, **kwargs):
        if self.context and self.context.get('user_id'):
            filter_rating = []
            for book_rating in data.ratings:
                if book_rating.user_id == self.context.get('user_id'):
                    filter_rating.append(book_rating)
            data.ratings = filter_rating
        return data
    