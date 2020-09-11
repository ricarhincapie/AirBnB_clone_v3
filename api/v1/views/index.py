#!/usr/bin/python3
"""Module to do something"""

from flask import Flask, jsonify, Blueprint
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {"Amenity": "amenities", "City": "cities",
           "Place": "places", "Review": "reviews",
           "State": "states", "User": "users"}


@app_views.route('/status', strict_slashes=False)
def status():
    """Manages /status routing"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns the stats for our application"""
    dic = {}
    for key, value in classes.items():
        dic[value] = storage.count(key)
    return jsonify(dic)
