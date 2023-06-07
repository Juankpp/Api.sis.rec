"""
Schemas to serialize/deserialize/validate models for the Tag module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields

from init_dep import ma
from .model import Tag

class TagSchema(ma.Schema):
    """Public schema for Tag model"""

    class Meta:
        """TagSchema meta data"""

        model = Tag

        # fields to expose
        fields = ('id', 'tag', 'timestamp', 'user', 'movie', 'movie_id')
        load_only = ['movie_id']
        dump_only = ['id']
        
    # nested schema
    user = fields.Nested(
        'UserSchema',
        only=('id', 'username'))

    # nested schema
    movie = fields.Nested(
        'MovieSchema',
        only=('id', 'title'))
    

    id = fields.UUID()
    movie_id = fields.Integer(required=True)
    tag = fields.String(required=True)
    