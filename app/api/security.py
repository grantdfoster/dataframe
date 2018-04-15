from functools import wraps
from flask_restful import abort
from flask import request


def process_header():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(403, message="Please provide an 'Authorization' header")
    else:
        return auth_header


def require_auth(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = process_header()
        return func(*args, **kwargs)
    return wrapper
