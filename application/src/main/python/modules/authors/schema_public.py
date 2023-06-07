"""
Schemas to serialize/deserialize/validate models for the Author module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields

from init_dep import ma
from .model import Author

class AuthorSchema(ma.Schema):
    """Public schema for Author model"""

    class Meta:
        """AuthorSchema meta data"""

        model = Author

        # fields to expose
        fields = ('id', 'name')
