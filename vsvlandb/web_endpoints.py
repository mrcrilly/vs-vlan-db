
from vsvlandb import app, dbo, vlans, subnets, sites
from vsvlandb.models import VLAN, Subnet, Site

from vsvlandb.forms import vlan, subnet, site

from flask import redirect, request, render_template, url_for, flash

import re
import ipaddress
import sys
import inspect

# Root/Index
@app.route('/')
def index():
    data = {
        'vlans': VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id)).limit(10),
        'subnets': Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id)).limit(10),
        'sites': Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id)).limit(10)
    }

    return render_template('index.html', data=data)

# VLANS
@app.route('/vlans')
def vlans_list():
    data = {
        'active': VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id)),
        'inactive': VLAN.query.filter_by(isactive=False).order_by(dbo.desc(VLAN.id))
    }

    return render_template('vlans_list.html', vlans=data)

@app.route('/vlans/add', methods=['GET', 'POST'])
def vlans_add():
    form = vlan.VlanForm()

    data = {}
    data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
    data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))

    form.subnet.choices = [(i.id,i.subnet) for i in data['subnets'].all()]
    form.site.choices = [(i.id,i.name) for i in data['sites'].all()]

    if form.validate_on_submit():
        vlans.add(form)
        return redirect('/vlans')
    else:
        for error in form.errors:
            for e in form.errors[error]:
                flash(u'{0}: {1}'.format(error, e), category='danger')


    data['vlans'] = VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id))

    return render_template('vlans_add.html', data=data, form=form)

@app.route('/vlans/edit/<int:vlanid>', methods=['GET', 'POST'])
def vlans_edit(vlanid):
    form = vlan.VlanForm()

    data = {}
    data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
    data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))

    form.subnet.choices = [(i.id,i.subnet) for i in data['subnets'].all()]
    form.site.choices = [(i.id,i.name) for i in data['sites'].all()]

    if form.validate_on_submit():
        vlans.edit(form, vlanid)
        return redirect('/vlans')
    else:
        for error in form.errors:
            for e in form.errors[error]:
                flash(u'{0}: {1}'.format(error, e), category='danger')

    # We need ALL VLANs here so we can edit non-active VLANs
    data['vlans'] = VLAN.query.filter_by().order_by(dbo.desc(VLAN.id))

    data['target'] = data['vlans'].filter_by(id=vlanid).limit(1).first()

    # We only want active VLANs in the topten side bar, so we now
    # refine the list to active VLANs
    data['vlans'] = data['vlans'].filter_by(isactive=True)

    form.vlanid.data = data['target'].vlan
    
    form.subnet.data = [(s.id,s.subnet) for s in data['target'].subnets]
    form.subnet.default = [s.id for s in data['target'].subnets]

    form.site.data = [(s.id,s.name) for s in data['target'].sites]
    form.site.default = [s.id for s in data['target'].sites]

    form.isactive.data = data['target'].isactive
    form.enhanced.data = data['target'].enhanced
    
    return render_template('vlans_edit.html', data=data, form=form)

@app.route('/vlans/delete/<int:vlanid>', methods=['GET', 'POST'])
def vlans_delete(vlanid):
    vlans.delete_id(vlanid)
    return redirect('/vlans')

# Subnets
@app.route('/subnets')
def subnets_list():
    lists = {
        'active': Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id)),
        'inactive': Subnet.query.filter_by(isactive=False).order_by(dbo.desc(Subnet.id)),
    }

    return render_template('subnets_list.html', subnets=lists)

@app.route('/subnets/add', methods=['GET', 'POST'])
def subnets_add():
    form = subnet.SubnetForm()

    data = {}
    data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
    data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))
    data['vlans'] = VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id))

    form.site.choices = [(i.id,i.name) for i in data['sites'].all()]

    if form.validate_on_submit():
        error = False
        
        try:
            ip = ipaddress.IPv4Network(form.subnet.data.decode())   
        except ipaddress.AddressValueError:
            flash(u"You provided an invalid IP address", category='danger')
            error = True
        except ipaddress.NetmaskValueError:
            flash(u"You provided an invalid netmask.", category='danger')
            error = True

        if error:
            return redirect('subnets/add')

        subnets.add(form)
        return redirect('/subnets')
    else:
        for error in form.errors:
            for e in form.errors[error]:
                flash(u'{0}: {1}'.format(error, e), category='danger')

    return render_template('subnets_add.html', data=data, form=form)

@app.route('/subnets/edit/<int:subnetid>', methods=['GET', 'POST'])
def subnets_edit(subnetid):
    form = subnet.SubnetForm()

    data = {}
    # data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
    data['vlans'] = VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id))
    data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))

    form.site.choices = [(i.id,i.name) for i in data['sites'].all()]

    if form.validate_on_submit():
        error = False
        
        try:
            ip = ipaddress.IPv4Network(form.subnet.data.decode())   
        except ipaddress.AddressValueError:
            flash(u"You provided an invalid IP address", category='danger')
            error = True
        except ipaddress.NetmaskValueError:
            flash(u"You provided an invalid netmask.", category='danger')
            error = True

        if error:
            return redirect('subnets/edit/{}'.format(subnetid))

        subnets.edit(form, vlanid)
        return redirect('/subnets')
    else:
        for error in form.errors:
            for e in form.errors[error]:
                flash(u'{0}: {1}'.format(error, e), category='danger')

    # We need ALL VLANs here so we can edit non-active VLANs
    data['subnets'] = Subnet.query.filter_by().order_by(dbo.desc(Subnet.id))

    data['target'] = data['subnets'].filter_by(id=subnetid).limit(1).first()

    # We only want active VLANs in the topten side bar, so we now
    # refine the list to active VLANs
    data['subnets'] = data['subnets'].filter_by(isactive=True)

    form.subnet.data = data['target'].subnet

    form.site.data = [(s.id,s.name) for s in data['target'].sites]
    form.site.default = [s.id for s in data['target'].sites]

    form.isactive.data = data['target'].isactive
    
    return render_template('subnets_edit.html', data=data, form=form)

@app.route('/subnets/delete/<int:subnetid>')
def subnets_delete(subnetid):
    subnets.delete_id(subnetid)
    return redirect('/subnets')


#Sites
@app.route('/sites')
def sites_list():
    lists = {
        'active': Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id)),
        'inactive': Site.query.filter_by(isactive=False).order_by(dbo.desc(Site.id)),
    }

    return render_template('sites_list.html', sites=lists)

@app.route('/sites/add', methods=['GET', 'POST'])
def sites_add():
    form = site.SiteForm()

    data = {}
    data['vlans'] = VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id))
    data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
    data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))

    if form.validate_on_submit():
        sites.add(form)
        return redirect('/sites')
    else:
        for error in form.errors:
            for e in form.errors[error]:
                flash(u'{0}: {1}'.format(error, e), category='danger')

    return render_template('sites_add.html', data=data, form=form)

@app.route('/sites/edit/<int:siteid>', methods=['GET', 'POST'])
def sites_edit(siteid):
    return render_template('sites_edit.html')

@app.route('/sites/delete/<int:siteid>', methods=['GET', 'POST'])
def sites_delete(siteid):
    return render_template('sites_delete.html')

# Coming soon.
# Impact
@app.route('/impacts')
def impact_list():
    pass

def impact_add():
    pass

def impact_edit():
    pass

def impact_delete():
    pass