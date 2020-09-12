#!/usr/bin/python3
"""
Module - User view RESTful API
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ display all users"""
    my_list = []
    for user in storage.all('User').values():
        my_list.append(user.to_dict())
    return jsonify(my_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_spec_user(user_id):
    """ gets an specific user by the user id given"""
    box = storage.get(User, user_id)
    if box is None:
        abort(404)
    else:
        return jsonify(box.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ delete user using the id given """
    box = storage.get(User, user_id)
    if box is None:
        abort(404)
    else:
        box.delete()
        storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ upload a new user """
    my_dict = request.get_json()
    if my_dict is None:
        abort(400, 'Not a JSON')
    elif 'email' not in my_dict:
        abort(400, 'Missing email')
    elif 'password' not in my_dict:
        abort(400, 'Missing password')
    create_user = User(**my_dict)
    create_user.save()
    return jsonify(create_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id=None):
    """ updates user by id with given information """
    ignore = ['id', 'email', 'created_at', 'updated_at']
    my_dict = request.get_json()
    if my_dict is None:
        abort(404, 'Not a JSON')
    box = storage.get(User, user_id)
    if box is None:
        abort(404)
    else:
        for key in my_dict.keys():
            if key not in ignore:
                setattr(box, key, my_dict[key])
        box.save()
        return jsonify(box.to_dict()) 200
