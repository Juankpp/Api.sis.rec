"""
Schemas to serialize/deserialize/validate models for the User module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from marshmallow import fields, validate

from init_dep import ma
from .model import User

class UserSchema(ma.Schema):
    """Public schema for User model"""

    class Meta:
        """UserSchema meta data"""

        model = User

        # fields to expose
        fields = ('id', 'username')

class RegisterUserSchema(ma.Schema):
    """Schema registration process"""

    class Meta:
        """RegisterUserSchema meta data"""

        # fields to expose
        fields = ('id', 'username', 'password',)
        dump_only = ['id', ]
        load_only = ['password',]

    # field validation
    id = fields.UUID()
    username = fields.String(
        required=True,
        validate=[
            validate.Length(
                2, 40,
                error="Value must be between 2 and 40 characters long.")
        ])
    password = fields.String(
        required=True)
