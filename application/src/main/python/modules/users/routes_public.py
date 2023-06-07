"""
Health Check public controllers.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from flask import jsonify, request, current_app
from marshmallow import ValidationError
from .schema_public import RegisterUserSchema
from .model import User
from init_dep import db
from sqlalchemy import func


def get_users():
    """Performs a basic system health check/smoke test.

    :returns: JSON string; status code
    :rtype: (str, int)
    """
    return jsonify({"success": True}), 200


def post_register_user():
    # make sure JSON POST data exists
    if request.json is None:
        return jsonify({"error": {"_schema": ["Invalid input type."]}}), 400

    json_data = {**request.json}

    if isinstance(json_data.get("username"), str):
        json_data["username"] = json_data.get("username").strip()

    if isinstance(json_data.get("username"), str):
        json_data["password"] = json_data.get("password").strip()

    errors = {}

    # validate data
    try:
        data = RegisterUserSchema().load(json_data)
    except ValidationError as err:
        errors = dict(list(errors.items()) + list(err.messages.items()))

    # return any errors
    if errors:
        return jsonify({"error": errors}), 400

    user_exist = User.query.filter(User.username == data.get("username")).first()

    if user_exist is not None:
        return jsonify({"error": {"username": ["Username already exists."]}}), 400 
    
    max_id = db.session.query(func.max(User.id)).scalar()    

    if max_id is None:
        max_id = 0
    
    # save registration
    user = User(
                id=max_id+1, 
                username=data.get("username"), 
                password=data.get("password"))
    
    # create user token for immediate access
    token = user.generate_auth_token(
        current_app.config['AUTH_TOKEN_EXPIRATION'])

    db.session.add(user)
    db.session.commit()
    user_dump = RegisterUserSchema().dump(user)
    user_dump['token'] = token.decode('ascii')
    user_dump['expiration'] = current_app.config['AUTH_TOKEN_EXPIRATION']

    
    print(user_dump)

    # response
    return jsonify({"registration": user_dump}), 201
