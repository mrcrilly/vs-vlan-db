
from vsvlandb import dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import flash

def addVlan(form):
    subnets = []
    sites = []

    if form.site.data:
        for site in form.site.data:
            site = Site.query.filter_by(id=site, isactive=True).limit(1)
            if site.count() == 1:
                sites.append(site.first())
    else:
        sites = False

    if form.subnet.data:
        for subnet in form.subnet.data:
            subnet = Subnet.query.filter_by(id=subnet, isactive=True).limit(1)
            if subnet.count() == 1:
                subnets.append(subnet.first())
    else:
        subnets = False

    if sites and subnets:
        for site in sites:
            for subnet in subnets:
                dbo.session.add(VLAN(form.vlanid.data, subnet=subnet, site=site, isactive=form.isactive.data, enhanced=form.enhanced.data))
                dbo.session.commit()
                flash("Added VLAN {0} to {1}".format(form.vlanid.data, subnet.subnet), category='success')

    if sites and not subnets:
        for site in sites:
            dbo.session.add(VLAN(form.vlanid.data, subnet=None, site=site, isactive=form.isactive.data, enhanced=form.enhanced.data))
            dbo.session.commit()
            flash("Added VLAN {0}".format(form.vlanid.data), category='success')

    if subnets and not sites:
        for subnet in subnets:
            dbo.session.add(VLAN(form.vlanid.data, subnet=subnet, site=None, isactive=form.isactive.data, enhanced=form.enhanced.data))
            dbo.session.commit()
            flash("Added VLAN {0}".format(form.vlanid.data), category='success')

    print form.vlanid.data
    if not sites and not subnets:
        dbo.session.add(VLAN(form.vlanid.data, subnet=None, site=None, isactive=form.isactive.data, enhanced=form.enhanced.data))
        dbo.session.commit()
        flash("Added VLAN {0}".format(form.vlanid.data), category='success')