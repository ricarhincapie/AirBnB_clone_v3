#!/usr/bin/python3
"""Module to do something"""

from flask import Flask, jsonify, Blueprint
from api.v1.views import app_views

#app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', strict_slashes=False)
def status():
    """Manages /status routing"""
    return jsonify({"status": "OK"})
