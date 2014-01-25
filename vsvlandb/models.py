
from vsvlandb import dbo

import ipaddress
import datetime

vlan_subnets = dbo.Table('vlan_subnets',
						 dbo.Column('subnet_id', dbo.Integer, dbo.ForeignKey('subnet.id')),
						 dbo.Column('vlan_id', dbo.Integer, dbo.ForeignKey('VLAN.id')))

vlan_sites = dbo.Table('vlan_sites',
						 dbo.Column('site_id', dbo.Integer, dbo.ForeignKey('site.id')),
						 dbo.Column('vlan_id', dbo.Integer, dbo.ForeignKey('VLAN.id')))

subnet_sites = dbo.Table('subnet_sites',
						 dbo.Column('subnet_id', dbo.Integer, dbo.ForeignKey('subnet.id')),
						 dbo.Column('site_id', dbo.Integer, dbo.ForeignKey('site.id')))

class VLAN(dbo.Model):

	id = dbo.Column(dbo.Integer, primary_key=True)

	vlan = dbo.Column(dbo.String(5))
	enhanced = dbo.Column(dbo.Boolean)
	impact = dbo.Column(dbo.String(5))
	isactive = dbo.Column(dbo.Boolean)

	subnets = dbo.relationship('Subnet', secondary=vlan_subnets, backref=dbo.backref('vlans', lazy='dynamic'))
	sites = dbo.relationship('Site', secondary=vlan_sites, backref=dbo.backref('vlans', lazy='dynamic'))

	added = dbo.Column(dbo.DateTime)

	def __init__(self, vlanid, subnets=[], sites=[], enhanced=False, impact=None, isactive=True):
		self.vlan = vlanid
		self.enhanced = enhanced
		self.isactive = isactive

		self.subnets = subnets
		self.sites = sites

		self.added = datetime.datetime.now()

	def __repr__(self):
		return '<VLAN {0}, {1}, {2}>'.format(self.vlan, self.subnet_id, self.site_id)

class Subnet(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)

	subnet = dbo.Column(dbo.String(30))
	netmask = dbo.Column(dbo.String(30))
	cidr = dbo.Column(dbo.String(30))
	size = dbo.Column(dbo.Integer)
	isactive = dbo.Column(dbo.Boolean)

	sites = dbo.relationship('Subnet', secondary=subnet_sites, backref=dbo.backref('subnets', lazy='dynamic'))

	def __init__(self, subnet, netmask, cidr=None, site=None, isactive=True):
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
	description = dbo.Column(dbo.String(30))
	isactive = dbo.Column(dbo.Boolean)

	def __init__(self, sitename, description=None, isactive=True):
		self.name = sitename
		self.isactive = isactive
		self.description = description

	def __repr__(self):
		return '<Site {0} ({1})>'.format(self.name, self.isactive)
        
class Impact(dbo.Model):
	id = dbo.Column(dbo.Integer, primary_key=True)
	name = dbo.Column(dbo.String, unique=True)
	description = dbo.Column(dbo.String(30))
	isactive = dbo.Column(dbo.Boolean)

	def __init__(self, impact, description=None, isactive=True):
		self.impact = impact
		self.isactive = isactive
		self.description = description

	def __repr__(self):
		return '<Impact {0} ({1})>'.format(self.impact, self.isactive)