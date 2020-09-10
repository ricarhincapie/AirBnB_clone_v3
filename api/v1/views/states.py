#!/usr/bin/python3
"""Module to do something"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State



@app_views.route('/states', strict_slashes=False)
def state_get_all():
    """Route to handle /states GET """
    my_list = []
    for item in storage.all("State").values():
        my_list.append(item.to_dict())
    return jsonify(my_list)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def state_get(state_id):
    """Route to handle states/id GET"""
    box = storage.get("State", state_id)
    if box is None:
        abort(404, 'Not found')
    else:
        return jsonify(box.to_dict())
