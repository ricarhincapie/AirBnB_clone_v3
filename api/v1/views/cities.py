#!/usr/bin/python3
"""Module to do something"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', strict_slashes=False)
def city_get_all(state_id):
    """Route to handle states/<state_id>/cities GET """
    my_list = []
    box = storage.get(State, state_id)
    if box is None:
        abort(404)
    cities = box.cities()
    for city in cities:
            my_list.append(city.to_dict())
    return jsonify(my_list)

@app_views.route('states/cities/<city_id>', strict_slashes=False)
def city_get(city_id):
    """Route to handle states/cities/city_id GET"""
    box = storage.get(City, city_id)
    if box is None:
        abort(404)
    else:
        return jsonify(box.to_dict()), 202

