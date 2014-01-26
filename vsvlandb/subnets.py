from vsvlandb import dbo
from vsvlandb.helpers import sitesAndSubnets
from vsvlandb.models import VLAN, Subnet, Site

import ipaddress
import sys

from flask import flash, redirect

def delete_id(subnet_id, flash_msg=True):
	subnet = Subnet.query.filter_by(id=subnet_id).limit(1).first()

	if subnet:
		dbo.session.delete(subnet)
		dbo.session.commit()

		if flash_msg:
			flash("Deleted Subnet {}".format(subnet.subnet), category='success')

def delete_subnet(subnet, flash_msg=True):
	subnets = Subnet.query.filter_by(subnet=subnet).all()

	if subnets:
		for subnet in subnets:
			dbo.session.delete(subnet)
			dbo.session.commit()

		if flash_msg:
			flash("Deleted subnet {}".format(subnet), category='success')

def edit(form, subnet_id, flash_msg=True):
	sites,subnets = sitesAndSubnets(form)

	if sites or subnets:
		delete_subnet(form.subnet.data, False)
		add(form, False)
	else:
		delete_id(subnet_id, False)
		add(form, False)

	if flash_msg:
		flash("Updated Subnet {0}".format(form.subnet.data), category='success')

def add(form, flash_msg=True):
	sites,subnets = sitesAndSubnets(form)

	subnet = ipaddress.IPv4Network(form.subnet.data.decode())
	subnet = Subnet(subnet=str(subnet), netmask=str(subnet.netmask), cidr=subnet.prefixlen,
					sites=sites, isactive=form.isactive.data)
	dbo.session.add(subnet)
	dbo.session.commit()

	if flash_msg:
		flash("Added Subnet {0}".format(form.subnet.data), category='success')