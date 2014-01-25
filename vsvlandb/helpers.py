from vsvlandb.models import VLAN, Subnet, Site

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