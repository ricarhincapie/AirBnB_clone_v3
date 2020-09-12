#!/usr/bin/python3
"""Module to start a Flask web app application"""

from flask import Flask, Blueprint, render_template
from flask import url_for, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """Manages app.teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def error_notFound(error):
    """Handles Not Found error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    app
    """
    app.run(host=host, port=port)
