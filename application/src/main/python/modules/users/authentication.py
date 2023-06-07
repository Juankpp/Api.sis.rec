"""
Authentication for Users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import g, current_app, abort
from flask_principal import Identity, RoleNeed, UserNeed, identity_changed

from .model import User


class Authentication:
    """Helper class for user authentication"""

    @staticmethod
    def verify_token(token):
        user = User.verify_auth_token(token)
        if not user:
            abort(401, "Bad token")

        # set global user
        g.user = user
        g.auth_scope = 'token'

        return user

    @staticmethod
    def verify_password(username_or_token, password):
        """Verifies that the requested user's password matches what is on file
        or that the access token is valid, and that the user's account is not
        locked.

        :param username_or_token: The user's username or access token
        :type username_or_token: str
        :param password: The user's password
        :type password: str
        :return: True on success or abort on failure
        :rtype: bool
        """

        if username_or_token is None:
            return None

        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:

            user = User.query.filter(
                User.username == username_or_token.strip()).first()
            # try to authenticate with username/password
            if not user or not user.check_password(password):
                # fail
                abort(401, "Bad credentials")

        # set global user
        g.user = user
        g.auth_scope = 'credentials'

        return user


  