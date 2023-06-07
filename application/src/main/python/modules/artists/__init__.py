"""
Artist module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_artists


def register(app):
    """Register artists routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public artists routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_artists', __name__)

    # GET /artists
    public.route("/artists", methods=['GET'])(get_artists)

    app.register_blueprint(public)
