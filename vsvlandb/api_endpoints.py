from vsvlandb import api

from flask import render_template, request
from flask.ext import restful

# Define our endpoints:

class ApiVLANs(restful.Resource):

    def get(self):
        return {'get': 'Not implemented'}

    def post(self):
    	return {'post': 'Not implemented'}

	def put(self):
		return {'put': 'Not implemented'}

	def delete(self):
		return {'delete': 'Not implemented'}

class ApiSubnets(restful.Resource):


    def get(self):
        pass

    def post(self):
    	return {'post': 'Not implemented'}

	def put(self):
		return {'put': 'Not implemented'}

	def delete(self):
		return {'delete': 'Not implemented'}

class ApiSites(restful.Resource):

    def get(self):
        return {'get': 'Not implemented'}

    def post(self):
    	return {'post': 'Not implemented'}

	def put(self):
		return {'put': 'Not implemented'}

	def delete(self):
		return {'delete': 'Not implemented'}

# Add them to the API:
api.add_resource(ApiVLANs, '/api/vlans/')
api.add_resource(ApiSubnets, '/api/subnets/')
api.add_resource(ApiSites, '/api/sites/')