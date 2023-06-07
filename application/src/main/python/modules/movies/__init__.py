"""
Movie module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint
from lib.auth import multi_auth
from .routes_public import get_movies, get_movies_recommended


def register(app):
    """Register movie routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public movie routes with the application.

    :param app: Flask application
    :type app: Flask
    """

    # pylint: disable=unused-variable
    public = Blueprint('public_movies', __name__)

    # GET /movies
    public.route("/movies", methods=['GET'])(
    public.route("/movies/<int:page>", methods=['GET'])(
        multi_auth.login_required(
            get_movies))) # noqa

    # GET /movies
    public.route("/movies/recommended", methods=['GET'])(
        multi_auth.login_required(
            get_movies_recommended))# noqa



    app.register_blueprint(public)
