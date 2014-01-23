from vsvlandb import api

from flask import render_template
from flask.ext import restful

# Define our endpoints:
class VLANs(restful.Resource):

    def get(self):
        return {'get': 'Not implemented'}

    def post(self):
    	return {'post': 'Not implemented'}

	def put(self):
		return {'put': 'Not implemented'}

	def delete(self):
		return {'delete': 'Not implemented'}

class Subnets(restful.Resource):

    def get(self):
        return {'get': 'Not implemented'}

    def post(self):
    	return {'post': 'Not implemented'}

	def put(self):
		return {'put': 'Not implemented'}

	def delete(self):
		return {'delete': 'Not implemented'}

class Sites(restful.Resource):

    def get(self):
        return {'get': 'Not implemented'}

    def post(self):
    	return {'post': 'Not implemented'}

	def put(self):
		return {'put': 'Not implemented'}

	def delete(self):
		return {'delete': 'Not implemented'}

# Add them to the API:
api.add_resource(VLANs, '/api/vlans/')
api.add_resource(Subnets, '/api/subnets/')
api.add_resource(Sites, '/api/sites/')