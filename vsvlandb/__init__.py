from flask import Flask
from flask.ext import restful, sqlalchemy, bcrypt

app = Flask(__name__)

api = restful.Api(app)
dbo = sqlalchemy.SQLAlchemy(app)
hsh = bcrypt.Bcrypt(app)

from vsvlandb import web_endpoints, api_endpoints