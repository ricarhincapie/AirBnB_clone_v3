#!/usr/bin/python3
"""
initialize the views package
"""
#from api.v1.views.index import app_views

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views import *
from api.v1.views.index import *
