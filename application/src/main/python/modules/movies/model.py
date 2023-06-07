"""
SQLAlchemy database record definitions for users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

from init_dep import db
from sqlalchemy.dialects.postgresql import UUID


# relation tables
relation_genres = db.Table(
    'movies_genres',
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movies.id'),
        primary_key=True),
    db.Column(
        'genre_id',
        UUID(as_uuid=True),
        db.ForeignKey('genres.id'),
        primary_key=True)
)

class Movie(db.Model):
    """Model for Movie"""

    __tablename__ = 'movies'
    
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
    year = db.Column(
        'year',
        db.Integer,
        nullable=False)
    genres = db.relationship(
        'Genre',
        secondary=relation_genres,
        order_by="Genre.genre")
    tags = db.relationship(
        'Tag',
        cascade='all,delete-orphan',
        back_populates='movie')
    ratings = db.relationship(
        'Rating',
        cascade='all,delete-orphan',
        back_populates='movie')