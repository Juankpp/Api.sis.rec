"""
BookRating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import post_book_rating, patch_book_rating
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
    public = Blueprint('public_book_ratings', __name__)

    # POST /book_rating
    public.route('/book_rating', methods=['POST'])(
        multi_auth.login_required(
            post_book_rating)) # noqa
    
    # PATCH /book_rating/{id}
    public.route('/book_rating/<uuid:book_rating_id>', methods=['PATCH'])(
        multi_auth.login_required(
            patch_book_rating))  # noqa

    app.register_blueprint(public)
