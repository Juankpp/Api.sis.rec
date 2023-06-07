"""
SQLAlchemy database record definitions for Rating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

import uuid

from sqlalchemy.dialects.postgresql import UUID


from init_dep import db

class Rating(db.Model):
    """Model for Rating"""

    __tablename__ = 'ratings'
    
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
    movie_id = db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movies.id'),
        nullable=False)

    user = db.relationship(
        'User',
        lazy='joined',
        back_populates='ratings')
    movie = db.relationship(
        'Movie',
        lazy='joined',
        back_populates='ratings')