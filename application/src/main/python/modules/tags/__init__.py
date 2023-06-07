"""
Tag module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_tags, post_tag
from lib.auth import multi_auth


def register(app):
    """Register tag routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public tag routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_tags', __name__)

    # GET /tags
    public.route("/tags", methods=['GET'])(get_tags)

    # POST /plans
    public.route('/tag', methods=['POST'])(
        multi_auth.login_required(
            post_tag)) # noqa


    app.register_blueprint(public)
