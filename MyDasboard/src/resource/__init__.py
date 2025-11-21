from flask import Blueprint
from flask_restful import Api

bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(bp)
