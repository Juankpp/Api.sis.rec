"""
Main application configuration.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=too-few-public-methods

import os


class Config:
    """Abstract data type containing configuration settings, data only"""
   
    # database properties
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234AAaa@localhost:5432/pgsis"
    AUTH_TOKEN_EXPIRATION = 140000
    AUTH_SECRET_KEY = "SECRET"

    