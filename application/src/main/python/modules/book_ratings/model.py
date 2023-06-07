"""
SQLAlchemy database record definitions for Rating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

import uuid

from sqlalchemy.dialects.postgresql import UUID


from init_dep import db

class BookRating(db.Model):
    """Model for BookRating"""

    __tablename__ = 'books_ratings'
    
    # columns
    id = db.Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    rating = db.Column(
        'rating',
        db.Float,
        nullable=False)
    timestamp = db.Column(
        'timestamp',
        db.TIMESTAMP(timezone=True),
        server_default=db.func.current_timestamp(),
        nullable=False)
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    book_id = db.Column(
        'book_id',
        db.Integer,
        db.ForeignKey('books.id'),
        nullable=False)
    
    # relationships
    user = db.relationship(
        'User',
        lazy='joined',
        back_populates='book_ratings')
    book = db.relationship(
        'Book',
        lazy='joined',
        back_populates='ratings')