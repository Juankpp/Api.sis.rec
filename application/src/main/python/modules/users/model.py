"""
SQLAlchemy database record definitions for users module.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import time
from authlib.jose import jwt


from init_dep import db
from config import Config

class User(db.Model):
    """Model for User"""

    __tablename__ = 'users'

    AUTH_SECRET_KEY = Config.AUTH_SECRET_KEY

    # columns
    id = db.Column(
        'id',
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False)
    username = db.Column(
        'username',
        db.String(40),
        index=True,
        unique=True,
        nullable=False)
    password = db.Column(
        'password',
        db.String(60),
        nullable=False)
    
    # relationships
    tags = db.relationship(
        'Tag',
        cascade='all,delete-orphan',
        back_populates='user')
    ratings = db.relationship(
        'Rating',
        cascade='all,delete-orphan',
        back_populates='user')
    book_ratings = db.relationship(
        'BookRating',
        cascade='all,delete-orphan',
        back_populates='user')
    song_ratings = db.relationship(
        'SongRating',
        cascade='all,delete-orphan',
        back_populates='user')


    def generate_auth_token(self, expiration=1800, scope='credentials'):
        """Creates a new authentication token.

        :param expiration: Length of time in seconds that token is valid
        :type expiration: int
        :param scope: Label of token's scope: credentials, otp, etc.
        :type scope: string
        :return: Authentication token
        :rtype: str
        """

        now = int(time.time())
        header = {'alg': 'HS256'}
        payload = {
            'iat': now,
            'exp': now + expiration,
            'id': self.id,
            'type': 'user',
            'scope': scope,
            'username': self.username,
        }
        return jwt.encode(header, payload, self.AUTH_SECRET_KEY)

    @staticmethod
    def verify_auth_token(token):
        """Verifies authentication token is valid and current.

        :param token: Authentication token
        :type token: str
        :return: The user associated with token if valid, None otherwise
        :rtype: User | None
        """

        now = int(time.time())

        try:
            claims = jwt.decode(token, User.AUTH_SECRET_KEY)
            if 'exp' not in claims or now > claims['exp']:
                return None
            if 'type' in claims and claims['type'] == 'user':
                user = User.query.get(claims['id'])
                user.claims = claims
                return user
        except Exception:
            pass
        return None

    def check_password(self, password):
        """Checks supplied password against saved value.

        :param password: User's plaintext password
        :type password: str
        :return: True if password matches what's on file, False otherwise
        :rtype: bool
        """
        print(password)
        print(self.password)

        return password == self.password