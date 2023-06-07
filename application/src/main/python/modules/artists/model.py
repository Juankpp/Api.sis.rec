"""
SQLAlchemy database record definitions for artists module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
import uuid

from sqlalchemy.dialects.postgresql import UUID

from init_dep import db

class Artist(db.Model):
    """Model for Artist"""

    __tablename__ = 'artists'

    # columns
    id = db.Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    name = db.Column(
        'name',
        db.String,
        unique=True,
        nullable=False)

    songs = db.relationship(
        'Song',
        cascade='all,delete-orphan',
        back_populates='artist')