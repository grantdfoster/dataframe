from flask import Flask

from app.api import api_bp, api_rest
app = Flask(__name__, static_url_path='')
app.register_blueprint(api_bp)
