"""
Tag module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import Blueprint

from .routes_public import get_books, patch_book, get_books_recommended
from lib.auth import multi_auth


def register(app):
    """Register book routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public_routes(app)


def public_routes(app):
    """Register public book routes with the application.

    :param app: Flask application
    :type app: Flask
    """
    public = Blueprint('public_books', __name__)
    
    # GET /books
    public.route("/books", methods=['GET'])(
    public.route("/books/<int:page>", methods=['GET'])(
        multi_auth.login_required(
            get_books))) # noqa

    # PATCH /book/{id}
    public.route('/book/<int:book_id>', methods=['PATCH'])(
        multi_auth.login_required(
            patch_book))  # noqa
    
    # GET /books
    public.route("/books/recommended", methods=['GET'])(
        multi_auth.login_required(
            get_books_recommended))# noqa
    
    app.register_blueprint(public)
