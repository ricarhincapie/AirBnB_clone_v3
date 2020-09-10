#!/usr/bin/python3
"""Module to do something"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def city_get_all(state_id):
    """Route to handle states/<state_id>/cities GET """
    my_list = []
    box = storage.get(State, state_id)
    if box is None:
        abort(404)
    cities = box.cities
    for city in cities:
            my_list.append(city.to_dict())
    return jsonify(my_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """get city information for specified city"""
    box = storage.get(City, city_id)
    if box is None:
        abort(404)
    return jsonify(box.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes the city w the id provided"""
    box = storage.get(City, city_id)
    if box:
        box.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Route to handle states/<state_id>/cities POST"""
    box = request.get_json(silent=True)
    if box is None:
        abort(400, 'Not a JSON')
    elif "name" not in box.keys():
        abort(400, 'Missing name')
    new_city = City(**box)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Route to handle states/<state_id>/cities POST"""
    requ = request.get_json(silent=True)
    if requ is None:
        abort(400, 'Not a JSON')
    current_city = storage.get(City, city_id)
    if current_city is None:
        abort(404, 'Not a JSON')
    for key, value in requ.items():
        if key in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        setattr(current_city, key, value)
    storage.save()
    return jsonify(current_city.to_dict()), 200
