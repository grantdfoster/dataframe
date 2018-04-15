""" API Blueprint Application """

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_bp', __name__)
api_rest = Api(api_bp)

@api_bp.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,Accept'
    return response

from app.api.rest import routing