"""
SongRating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import post_song_rating, patch_song_rating
from lib.auth import multi_auth

def register(app):
    """Register rating routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public rating routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_song_ratings', __name__)

    # POST /song_rating
    public.route('/song_rating', methods=['POST'])(
        multi_auth.login_required(
            post_song_rating)) # noqa
    
    # PATCH /song_rating/{id}
    public.route('/song_rating/<uuid:song_rating_id>', methods=['PATCH'])(
        multi_auth.login_required(
            patch_song_rating))  # noqa

    app.register_blueprint(public)
