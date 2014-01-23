
from vsvlandb import dbo

import ipaddress
import datetime

class VLAN(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)

	vlan = dbo.Column(dbo.String(5), unique=True)
	enhanced = dbo.Column(dbo.Boolean)
	impact = dbo.Column(dbo.String(5))
	isactive = dbo.Column(dbo.Boolean)

	subnet_id = dbo.Column(dbo.Integer, dbo.ForeignKey('subnet.id'))
	subnet = dbo.relationship('Subnet', backref='vlan', lazy='joined')

	site_id = dbo.Column(dbo.Integer, dbo.ForeignKey('site.id'))
	site = dbo.relationship('Site', backref='vlan', lazy='joined')

	added = dbo.Column(dbo.DateTime)

	def __init__(self, vlanid, subnet, site, enhanced=False, impact=None, isactive=True):
		self.vlan = vlanid
		self.enhanced = enhanced
		self.isactive = isactive

		self.subnet = subnet
		self.site = site

		self.added = datetime.datetime.now()

	def __repr__(self):
		return '<VLAN {}>'.format(self.vlanid)

class Subnet(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)

	subnet = dbo.Column(dbo.String(30), unique=True)
	netmask = dbo.Column(dbo.String(30))
	cidr = dbo.Column(dbo.String(30))
	size = dbo.Column(dbo.Integer)
	isactive = dbo.Column(dbo.Boolean)

	site_id = dbo.Column(dbo.Integer, dbo.ForeignKey('site.id'))
	site = dbo.relationship('Site', backref='subnet', lazy='joined')

	def __init__(self, subnet, netmask, site, cidr=None, isactive=True):
		self.subnet = subnet
		self.netmask = netmask
		self.cidr = cidr
		self.isactive = isactive

		self.site = site

	def __repr__(self):
		return '<Subnet {0}/{1}>'.format(self.subnet, self.netmask)

class Site(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)
	name = dbo.Column(dbo.String, unique=True)
	description = dbo.Column(dbo.String)
	isactive = dbo.Column(dbo.Boolean)

	def __init__(self, sitename, description=None, isactive=True):
		self.name = sitename
		self.isactive = isactive
		self.description = description

	def __repr__(self):
		return '<Site {0} ({1})>'.format(self.sitename, self.isactive)