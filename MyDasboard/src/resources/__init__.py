from flask import Blueprint
from flask_restful import Api

bp = Blueprint("api", __name__, url_prefix="/mydashboard/api/v1")
api = Api(bp)

# Import modules to register routes
from . import devices
