
from vsvlandb import dbo

import ipaddress
import datetime

vlan_subnets = dbo.Table('vlan_subnets',
                         dbo.Column('subnet_id', dbo.Integer, dbo.ForeignKey('subnet.id')),
                         dbo.Column('vlan_id', dbo.Integer, dbo.ForeignKey('VLAN.id')))

vlan_sites = dbo.Table('vlan_sites',
                       dbo.Column('site_id', dbo.Integer, dbo.ForeignKey('site.id')),
                       dbo.Column('vlan_id', dbo.Integer, dbo.ForeignKey('VLAN.id')))

vlan_impacts = dbo.Table('vlan_impacts',
                        dbo.Column('impact_id', dbo.Integer, dbo.ForeignKey('impact.id')),
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
    
    # impacts = dbo.relationship('Impact', secondary=vlan_impacts, backref=dbo.backref('vlans', lazy='dynamic'))
    impact_id = dbo.Column(dbo.Integer, dbo.ForeignKey('impact.id'))
    impact = dbo.relationship('Impact', backref=dbo.backref('vlan', order_by=id))

    description = dbo.Column(dbo.String(50))

    added = dbo.Column(dbo.DateTime)

    def __init__(self, vlan, subnets=[], sites=[], impact=None, enhanced=False, isactive=True, description=None):
        self.vlan = vlan
        self.enhanced = enhanced
        self.isactive = isactive

        self.subnets = subnets
        self.sites = sites
        self.impact = impact

        self.added = datetime.datetime.now()

        self.description = description

    def __repr__(self):
        return '<VLAN {}>'.format(self.vlan)

class Subnet(dbo.Model):
    id = dbo.Column(dbo.Integer, primary_key=True)

    subnet = dbo.Column(dbo.String(30))
    netmask = dbo.Column(dbo.String(30))
    cidr = dbo.Column(dbo.String(30))
    size = dbo.Column(dbo.Integer)
    isactive = dbo.Column(dbo.Boolean)
    description = dbo.Column(dbo.String(50))

    sites = dbo.relationship('Site', secondary=subnet_sites, backref=dbo.backref('subnets', lazy='dynamic'))

    def __init__(self, subnet, sites=[], description=None, isactive=True):
        self.subnet = str(subnet)
        self.netmask = str(subnet.netmask)
        self.cidr = str(subnet.prefixlen)
        self.isactive = isactive
        self.description = description

        self.sites = sites

    def __repr__(self):
        return '<Subnet {0}/{1}>'.format(self.subnet, self.netmask)

class Site(dbo.Model):
    id = dbo.Column(dbo.Integer, primary_key=True)

    name = dbo.Column(dbo.String(30), unique=True)
    description = dbo.Column(dbo.String(30))
    isactive = dbo.Column(dbo.Boolean)

    def __init__(self, name, description=None, isactive=True):
        self.name = name
        self.isactive = isactive
        self.description = description

    def __repr__(self):
        return '<Site {0} ({1})>'.format(self.name, self.isactive)
        
class Impact(dbo.Model):
    id = dbo.Column(dbo.Integer, primary_key=True)
    name = dbo.Column(dbo.String(30), unique=True)
    description = dbo.Column(dbo.String(30))
    isactive = dbo.Column(dbo.Boolean)

    def __init__(self, name, description=None, isactive=True):
        self.name = name
        self.isactive = isactive
        self.description = description

    def __repr__(self):
        return '<Impact Level {0} ({1})>'.format(self.name, self.isactive)