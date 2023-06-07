"""
Schemas to serialize/deserialize/validate models for the Artist module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""


from init_dep import ma
from .model import Artist

class ArtistSchema(ma.Schema):
    """Public schema for Artist model"""

    class Meta:
        """ArtistSchema meta data"""

        model = Artist

        # fields to expose
        fields = ('id', 'name')
