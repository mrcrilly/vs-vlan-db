
from vsvlandb import app, dbo, vlans
from vsvlandb.models import VLAN, Subnet, Site
from vsvlandb.forms.vlan import VlanForm

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
        'active': VLAN.query.filter_by(isactive=True),
        'inactive': VLAN.query.filter_by(isactive=False)
    }

    return render_template('vlans_list.html', vlans=data)

@app.route('/vlans/add', methods=['GET', 'POST'])
def vlans_add():
    form = VlanForm()

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
    form = VlanForm()

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

    print form.subnet.default

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
        'active': (Subnet.query.filter_by(isactive=True).count(), Subnet.query.filter_by(isactive=True)),
        'inactive': (Subnet.query.filter_by(isactive=False).count(), Subnet.query.filter_by(isactive=False)),
    }
    return render_template('subnets_list.html', subnets=lists)

@app.route('/subnets/add', methods=['GET', 'POST'])
def subnets_add():
    if request.method == 'GET':
        data = {
            'error': {}
        }

        data['subnets'] = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id))
        data['sites'] = Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id))
        data['vlans'] = VLAN.query .filter_by(isactive=True).order_by(dbo.desc(VLAN.id))

        return render_template('subnets_add.html', data=data)
    else:
        subnet = None
        netmask = None
        sites = []
        isactive = False

        if 'subnet' in request.form:
            ip = None
            error = False

            try:
                ip = ipaddress.IPv4Network(request.form['subnet'].decode())
            except ipaddress.AddressValueError:
                flash(u"You provided an invalid IP address", category='danger')
                error = True
            except ipaddress.NetmaskValueError:
                flash(u"You provided an invalid netmask.", category='danger')
                error = True
            except:
                flash(u"Exception caught: {}".format(sys.exc_info()[0]), category='danger')
                error = True

            if error:
                return redirect('/subnets/add')
            else:
                subnet = ip
        else:
            flash(u"You need to supply a subnet to add a subnet.", category='danger')
            return redirect('/subnets/add')

        if 'site' in request.form:
            selections = request.form.getlist('site')
            for selection in selections:
                if re.match(r'^[0-9]{1,}$', selection):
                    site = Site.query.filter_by(id=selection).limit(1)
                    if site.count() >= 1:
                        sites.append(site.first())
                else:
                    data['error']['badsiteid'] = True
                    flash(u"Bad Site ID: {}. Please make your selection again.".format(selection), category='danger')
        else:
            sites = False

        if 'active' in request.form:
            if re.match(r'^on$', request.form['active']):
                isactive = True
            else:
                isactive = False

        if sites:
            for site in sites:
                newsubnet = Subnet(subnet=str(subnet), netmask=str(subnet.netmask), cidr=subnet.prefixlen, site=site, isactive=isactive)
                dbo.session.add(newsubnet)
                dbo.session.commit()

                flash(u"Added subnet {0} to {1}".format(str(subnet), site), category='success')
        else:
            newsubnet = Subnet(subnet=str(subnet), netmask=str(subnet.netmask), cidr=subnet.prefixlen, site=None, isactive=isactive)
            dbo.session.add(newsubnet)
            dbo.session.commit()

            flash(u"Added subnet {0}".format(str(subnet)), category='success')

    return redirect('/subnets')

@app.route('/subnets/edit/<int:subnetid>')
def subnets_edit(subnetid):
    return render_template('subnets_edit.html')

@app.route('/subnets/delete/<int:subnetid>')
def subnets_delete(subnetid):
    return render_template('subnets_delete.html')



#Sites
@app.route('/sites')
def sites_list():
    lists = {
        'active': (Site.query.filter_by(isactive=True).count(), Site.query.filter_by(isactive=True)),
        'inactive': (Site.query.filter_by(isactive=False).count(), Site.query.filter_by(isactive=False)),
    }
    return render_template('sites_list.html', sites=lists)

@app.route('/sites/add', methods=['GET', 'POST'])
def sites_add():
    if request.method == 'GET':
        return render_template('sites_add.html')
    else:
        site = Site(request.form['site'])
        dbo.session.add(site)
        dbo.session.commit()

        return redirect('/sites')

@app.route('/sites/edit/<int:siteid>')
def sites_edit(siteid):
    return render_template('sites_edit.html')

@app.route('/sites/delete/<int:siteid>')
def sites_delete(siteid):
    return render_template('sites_delete.html')

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