
from vsvlandb import dbo

class VLAN(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)
	vlanid = dbo.Column(dbo.String(5), unique=True)

	def __init__(self, vlanid):
		self.vlanid = vlanid

	def __repr__(self):
		return '<VLAN {}>'.format(self.vlanid)

class Subnet(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)
	subnet = dbo.Column(dbo.String, unique=True)

	def __init__(self, subnet):
		self.subnet = subnet

	def __repr__(self):
		return '<Subnet {}>'.format(self.subnet)

class Site(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)
	sitename = dbo.Column(dbo.String, unique=True)

	def __init__(self, sitename):
		self.sitename = sitename

	def __repr__(self):
		return '<Site {}>'.format(self.sitename)