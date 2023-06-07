"""
SQLAlchemy database record definitions for authors module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
import uuid

from sqlalchemy.dialects.postgresql import UUID

from init_dep import db

class Author(db.Model):
    """Model for Author"""

    __tablename__ = 'authors'

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

    books = db.relationship(
        'Book',
        cascade='all,delete-orphan',
        back_populates='author')