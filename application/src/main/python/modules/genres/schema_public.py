"""
Schemas to serialize/deserialize/validate models for the Genre module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""


from init_dep import ma
from .model import Genre


class GenreSchema(ma.Schema):
    """Public schema for Genre model"""

    class Meta:
        """GenreSchema meta data"""

        model = Genre

        # fields to expose
        fields = ('id', 'genre')

