"""
SQLAlchemy database record definitions for users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

import uuid

from sqlalchemy.dialects.postgresql import UUID

from init_dep import db

class Song(db.Model):
    """Model for Song"""

    __tablename__ = 'songs'
    
    # columns
    id = db.Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    song = db.Column(
        'song',
        db.Text(),
        nullable=False)
    link = db.Column(
        'link',
        db.Text(),
        nullable=False)
    text = db.Column(
        'text',
        db.Text(),
        nullable=False)
    artist_id = db.Column(
        'artist_id',
        UUID(as_uuid=True),
        db.ForeignKey('artists.id'),
        nullable=False)

    artist = db.relationship(
        'Artist',
        lazy='joined',
        back_populates='songs')
    ratings = db.relationship(
        'SongRating',
        cascade='all,delete-orphan',
        back_populates='song')
