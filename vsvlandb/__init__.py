from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

from vsvlandb import web_endpoints, api_endpoints