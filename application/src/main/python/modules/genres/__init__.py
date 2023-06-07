"""
Genre module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_genres


def register(app):
    """Register genre routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public genre routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_genres', __name__)

    # GET /genres
    public.route("/genres", methods=['GET'])(get_genres)

    app.register_blueprint(public)
