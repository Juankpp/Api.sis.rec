"""
SQLAlchemy database record definitions for books module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from sqlalchemy.dialects.postgresql import UUID

from init_dep import db

class Book(db.Model):
    """Model for Book"""

    __tablename__ = 'books'
    
    # columns
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False)
    title = db.Column(
        'title',
        db.String,
        nullable=False)
    average_rating = db.Column(
        'average_rating',
        db.Float,
        nullable=False)
    ratings_count = db.Column(
        'ratings_count',
        db.Integer,
        nullable=False)    
    text_reviews_count = db.Column(
        'text_reviews_count',
        db.Integer,
        nullable=False) 
    publisher = db.Column(
        'publisher',
        db.String,
        nullable=False)


    author_id = db.Column(
        'author_id',
        UUID(as_uuid=True),
        db.ForeignKey('authors.id'),
        nullable=False)
    author = db.relationship(
        'Author',
        lazy='joined',
        back_populates='books')
    ratings = db.relationship(
        'BookRating',
        cascade='all,delete-orphan',
        back_populates='book')