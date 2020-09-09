#!/usr/bin/python3
"""Module to start a Flask web app application"""

from flask import Flask, Blueprint, render_template, url_for
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """Manages app.teardown_appcontext"""
    storage.close()


if __name__ == "__main__":
    """
    app
    """
    app.run(host=host, port=port)
