"""
SQLAlchemy database record definitions for users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=no-member,too-few-public-methods

import uuid

from sqlalchemy.dialects.postgresql import UUID

from init_dep import db

class Genre(db.Model):
    """Model for Genre"""

    __tablename__ = 'genres'
    
    # columns
    id = db.Column(
        'id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    genre = db.Column(
        'genre',
        db.String,
        unique=True,
        nullable=False)

    
    