"""
Author module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_authors


def register(app):
    """Register authors routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public authors routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_authors', __name__)

    # GET /authors
    public.route("/authors", methods=['GET'])(get_authors)

    app.register_blueprint(public)
