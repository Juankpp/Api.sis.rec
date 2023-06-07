"""
Rating module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import post_rating, patch_rating
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
    public = Blueprint('public_ratings', __name__)

    # POST /rating
    public.route('/rating', methods=['POST'])(
        multi_auth.login_required(
            post_rating)) # noqa
    
    # PATCH /rating/{id}
    public.route('/rating/<uuid:rating_id>', methods=['PATCH'])(
        multi_auth.login_required(
            patch_rating))  # noqa

    app.register_blueprint(public)
