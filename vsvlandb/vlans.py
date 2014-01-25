
from vsvlandb import dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import flash

def delete_id(vlan_id, flash_msg=True):
	vlan = VLAN.query.filter_by(id=vlan_id).limit(1).first()

	if vlan:
		dbo.session.delete(vlan)
		dbo.session.commit()

		if flash_msg:
			flash("Deleted VLAN {}".format(vlan.vlan), category='success')

def delete_vlan(vlan, flash_msg=True):
	vlans = VLAN.query.filter_by(vlan=vlan).all()

	if vlans:
		for vlan in vlans:
			dbo.session.delete(vlan)
			dbo.session.commit()

		if flash_msg:
			flash("Deleted VLAN {}".format(vlan), category='success')

def edit(form, vlan_id, flash_msg=True):
	sites,subnets = sitesAndSubnets(form)

	if sites or subnets:
		delete_vlan(form.vlanid.data, False)
		add(form, False)
	else:
		delete_id(vlan_id, False)
		add(form, False)

	if flash_msg:
		flash("Updated VLAN {0}".format(form.vlanid.data), category='success')

def add(form, flash_msg=True):
	sites,subnets = sitesAndSubnets(form)

	vlan = VLAN(form.vlanid.data, subnets=subnets, sites=sites, isactive=form.isactive.data, enhanced=form.enhanced.data)
	dbo.session.add(vlan)
	dbo.session.commit()

	if flash_msg:
		flash("Added VLAN {0}".format(form.vlanid.data), category='success')

def sitesAndSubnets(form):
	subnets = []
	sites = []

	if form.site.data:
	    for site in form.site.data:
	        site = Site.query.filter_by(id=site, isactive=True).limit(1)
	        if site.count() == 1:
	            sites.append(site.first())

	if form.subnet.data:
	    for subnet in form.subnet.data:
	        subnet = Subnet.query.filter_by(id=subnet, isactive=True).limit(1)
	        if subnet.count() == 1:
	            subnets.append(subnet.first())

	return sites, subnets
