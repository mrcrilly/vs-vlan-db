from vsvlandb import api

from flask.ext import restful

# Define our endpoints:
class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

# Add them to the API:
api.add_resource(HelloWorld, '/')