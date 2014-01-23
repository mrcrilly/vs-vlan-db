from flask import Flask
from flask.ext import restful, sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/vlan.db'

api = restful.Api(app)
dbo = sqlalchemy.SQLAlchemy(app)

from vsvlandb import web_endpoints, api_endpoints