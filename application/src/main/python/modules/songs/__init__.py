"""
Song module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_songs, get_songs_recommended, \
    get_songs_recommended_based_content
from lib.auth import multi_auth


def register(app):
    """Register song routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public song routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_songs', __name__)

    # GET /songs
    public.route("/songs", methods=['GET'])(

    public.route("/songs/<int:page>", methods=['GET'])(
        multi_auth.login_required(
            get_songs))) # noqa

    # GET /songs
    public.route("/songs/recommended", methods=['GET'])(
        multi_auth.login_required(
            get_songs_recommended))# noqa

    # GET /songs
    public.route("/songs/recommended/content", methods=['GET'])(
        multi_auth.login_required(
            get_songs_recommended_based_content))# noqa




    app.register_blueprint(public)

