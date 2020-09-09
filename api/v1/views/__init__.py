#!/usr/bin/python3
"""
initialize the views package
"""
from api.v1.views.index import app_views
"""
from flask import Blueprint
from api.v1.views import *
from api.v1.views.index import *

app_views = Blueprint('first', url_prefix='/api/v1')
"""