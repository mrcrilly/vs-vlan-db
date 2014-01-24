
from vsvlandb import app, dbo, vlan_helpers
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
        'vlans': VLAN.query.limit(10).all(),
        'subnets': Subnet.query.limit(10).all(),
        'sites': Site.query.limit(10).all()
    }

    return render_template('index.html', lists=data)

# VLANS
@app.route('/vlans')
def vlans():
    data = {
        'active': (VLAN.query.filter_by(isactive=True).count(), VLAN.query.filter_by(isactive=True)),
        'inactive': (VLAN.query.filter_by(isactive=False).count(), VLAN.query.filter_by(isactive=False))
    }

    return render_template('vlans_list.html', vlans=data)

@app.route('/vlans/add', methods=['GET', 'POST'])
def vlans_add():
    form = VlanForm()

    data = {}
    data['subnets'] = Subnet.query.filter_by(isactive=True)
    data['sites'] = Site.query.filter_by(isactive=True)
    data['vlans'] = VLAN.query.filter_by(isactive=True)

    form.subnet.choices = [(i.id,i.subnet) for i in data['subnets'].all()]
    form.site.choices = [(i.id,i.name) for i in data['sites'].all()]

    if form.validate_on_submit():
        vlan_helpers.addVlan(form)
        return redirect('/vlans')
    else:
        for error in form.errors:
            for e in form.errors[error]:
                flash(u'{0}: {1}'.format(error, e), category='danger')


    return render_template('vlans_add.html', data=data, form=form)

@app.route('/vlans/edit/<int:vlanid>', methods=['GET', 'POST'])
def vlans_edit(vlanid):
    form = VlanForm()

    data = {}
    data['subnets'] = Subnet.query.filter_by(isactive=True)
    data['sites'] = Site.query.filter_by(isactive=True)
    data['vlans'] = VLAN.query.filter_by(isactive=True)

    vlan = VLAN.query.filter_by(id=vlanid).limit(1).first()

    form.vlanid.data = vlan.id
    form.subnet.choices = [(i.id,i.subnet) for i in data['subnets'].all()]
    form.subnet.data = [i.id for i in Subnet.query.filter_by(id=vlan.subnet_id)]
    form.site.choices = [(i.id,i.name) for i in data['sites'].all()]
    form.site.data = [i.id for i in Site.query.filter_by(id=vlan.site_id)]
    form.isactive.data = vlan.isactive
    form.enhanced.data = vlan.enhanced
    
    if form.validate_on_submit():
        pass

    return render_template('vlans_edit.html', data=data, form=form)

@app.route('/vlans/delete/<int:vlanid>', methods=['GET', 'POST'])
def vlans_delete(vlanid):
    if request.method == 'GET':
        vlan = VLAN.query.filter_by(id=vlanid).first()
        return render_template('vlans_delete.html', vlan=vlan)
    else:
        vlan = VLAN(int(request.form['vlanid']))
        dbo.session.add(vlan)
        dbo.session.commit()

        return redirect('/vlans')


# Subnets
@app.route('/subnets')
def subnets():
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

        data['subnets'] = Subnet.query.filter_by(isactive=True)
        data['sites'] = Site.query.filter_by(isactive=True)
        data['vlans'] = VLAN.query .filter_by(isactive=True)

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
def sites():
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
