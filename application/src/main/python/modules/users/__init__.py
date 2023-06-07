"""
Health check module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_users
from lib.auth import auth_basic, auth_token, multi_auth
from .authentication import Authentication
from .routes_auth import get_auth_token, get_auth_token_check
from .routes_public import post_register_user


def register(app):
    """Register health check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public health check routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    
    @auth_basic.verify_password
    def verify_password(username, password):
        return Authentication.verify_password(username, password)

    @auth_token.verify_token
    def verify_token(token):
        return Authentication.verify_token(token)


    public = Blueprint('public_users', __name__)

    # GET /users
    public.route("/users", methods=['GET'])(get_users)

    # GET /token
    public.route('/token', methods=['GET'])(
            multi_auth.login_required(
            get_auth_token))  # noqa

    # GET /token/check
    public.route('/token/check', methods=['GET'])(
            multi_auth.login_required(
            get_auth_token_check))  # noqa

    # GET /token/check
    public.route('/register', methods=['POST'])(
            post_register_user)  # noqa

    app.register_blueprint(public)
