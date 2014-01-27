from vsvlandb import dbo
from vsvlandb.helpers import sitesAndSubnets
from vsvlandb.models import VLAN, Site, Site

import ipaddress
import sys

from flask import flash, redirect

def delete_id(site_id, flash_msg=True):
    site = Site.query.filter_by(id=site_id).limit(1).first()

    if site:
        dbo.session.delete(site)
        dbo.session.commit()

        if flash_msg:
            flash("Deleted Site {}".format(site.name), category='success')

def delete_site(site, flash_msg=True):
    sites = Site.query.filter_by(name=site).all()

    if sites:
        for site in sites:
            dbo.session.delete(site)
            dbo.session.commit()

        if flash_msg:
            flash("Deleted site {}".format(site), category='success')

def edit(form, site_id, flash_msg=True):
    delete_id(site_id, False)
    add(form, False)

    if flash_msg:
        flash("Updated Site {0}".format(form.name.data), category='success')

def add(form, flash_msg=True):
    pass