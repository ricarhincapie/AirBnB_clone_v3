#!/usr/bin/python3
"""Module to do something"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Route to handle /amenities GET """
    my_list = []
    for item in storage.all("Amenity").values():
        my_list.append(item.to_dict())
    return jsonify(my_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenitie(amenity_id):
    """Route to handle /amenities/id GET """
    box = storage.get(Amenity, amenity_id)
    if box is None:
        abort(404)
    return jsonify(box.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id=None):
    """Route to handle /amenities/id DELETE """
    box = storage.get(Amenity, amenity_id)
    if box is None:
        abort(404)
    else:
        storage.delete(box)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenitie():
    """Route to handle /amenities POST """
    requ = request.get_json(silent=True)
    if not requ:
        abort(400, 'Not a JSON')
    if not requ.get("name"):
        abort(400, 'Missing name')
    else:
        new_amenitie = Amenity(**requ)
        storage.new(new_amenitie)
        storage.save()
    return jsonify(new_amenitie.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenitie(amenity_id):
    """Route to handle /amenities/id PUT """
    requ = request.get_json(silent=True)
    if not requ:
        abort(400, 'Not a JSON')
    box = storage.get(Amenity, amenity_id)
    if not box:
        abort(404)
    else:
        for key, value in requ.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            setattr(box, key, value)
        storage.save()
        return jsonify(box.to_dict()), 200
