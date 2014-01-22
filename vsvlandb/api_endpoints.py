from vsvlandb import api

from flask import render_template
from flask.ext import restful

# Define our endpoints:
class HelloWorld(restful.Resource):
    def get(self):
        return render_template('base.html', name='Michael')

# Add them to the API:
api.add_resource(HelloWorld, '/api/')