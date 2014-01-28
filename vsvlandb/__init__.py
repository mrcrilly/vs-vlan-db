from flask import Flask
from flask.ext import restful, sqlalchemy

app = Flask(__name__)
api = restful.Api(app)
dbo = sqlalchemy.SQLAlchemy(app)

from vsvlandb import web_endpoints, api_endpoints