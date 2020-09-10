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


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def state_get(state_id):
    """Route to handle states/id GET"""
    box = storage.get(State, state_id)
    if box is None:
        abort(404, 'Not found')
    else:
        return jsonify(box.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """Route to handle /states/id DELETE"""
    box = storage.get(State, state_id)
    if box is None:
        abort(404, 'Not found')
    storage.delete(box)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """Route to handle /states POST"""
    box = request.get_json(silent=True)
    if box is None:
        abort(400, 'Not a JSON')
    elif 'name' not in box.keys():
        abort(400, 'Missing name')
    else:
        new_state = State(**box)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def state_update(state_id=None):
    """Route to handle /states/id PUT"""
    box = request.get_json(silent=True)
    if box is None:
        abort(400, 'Not a JSON')
    current_state = storage.get(State, state_id)
    if current_state is None:
        abort(404)
    else:
        for key, value in box.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(current_state, key, value)
        storage.save()
        dic_current_st = current_state.to_dict()
    return make_response(jsonify(dic_current_st), 200)
