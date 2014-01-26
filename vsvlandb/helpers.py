from vsvlandb import dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import flash

def sitesAndSubnets(form):
	subnets = []
	sites = []

	if form.sites.data:
	    for site in form.sites.data:
	        site = Site.query.filter_by(id=site, isactive=True).limit(1)
	        if site:
	            sites.append(site.first())

	if form.subnet.data:
	    for subnet in form.subnet.data:
	        subnet = Subnet.query.filter_by(id=subnet, isactive=True).limit(1)
	        if subnet:
	            subnets.append(subnet.first())

	return sites, subnets

def top_ten():
	data = {}
	data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
	data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))
	data['vlans'] = VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id))

	return data

def flash_errors(errors):
	for error in errors:
		for e in errors[error]:
			flash(u'{0}: {1}'.format(error, e), category='danger')