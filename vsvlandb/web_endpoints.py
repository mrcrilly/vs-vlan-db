
from vsvlandb import app, dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import redirect, request, render_template, url_for, flash

import re
import ipaddress
import sys

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
    if request.method == 'GET':
        data = {
            'error': {}
        }

        data['subnets'] = Subnet.query.filter_by(isactive=True)
        data['sites'] = Site.query.filter_by(isactive=True)

        vlans = VLAN.query.filter_by(isactive=True)
        if vlans.count() >= 1:
            data['vlans'] = vlans

        return render_template('vlans_add.html', data=data)

    if request.method == 'POST':
        data = {
            'error': {}
        }

        vlanid = None 
        subnets = []
        sites = []
        isactive = False
        enhanced = False

        if 'vlanid' in request.form:
            if re.match(r'^[0-9]{1,5}$', request.form['vlanid']):
                vlanid = request.form['vlanid']
            else:
                data['error']['badvlanid'] = True
                flash(u"Bad VLAN ID: {}. Please try again.".format(vlanid), category='danger')
                return redirect('/vlans/add')
        else:
            data['error']['badvlanid'] = True
            flash(u"Missing vLAN ID. Please try again.", category='danger')
            return redirect('/vlans/add')

        if 'subnet' in request.form:
            selections = request.form.getlist('subnet')
            for selection in selections:
                if re.match(r'^[0-9]{1,}$', selection):
                    subnet = Subnet.query.filter_by(id=selection).limit(1)
                    if subnet.count() >= 1:
                        subnets.append(subnet.first())
                else:
                    data['error']['badsubnetid'] = True
                    flash(u"Bad Subnet ID: {}. Please make your selection again.".format(selection), category='danger')
        else:
            subnets = False

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

        if 'enhanced' in request.form:
            if re.match(r'^on$', request.form['enhanced']):
                enhanced = True
            else:
                enhanced = False

        if sites and subnets:
            for site in sites:
                for subnet in subnets:
                    vlan = VLAN(vlanid, subnet=subnet, site=site, isactive=isactive, enhanced=enhanced)
                    dbo.session.add(vlan)
                    dbo.session.commit()
                    flash("Added {0} to {1} in {2}".format(vlanid, subnet.subnet, site.name), category='success')

        if sites and not subnets:
            for site in sites:
                vlan = VLAN(vlanid, subnet=None, site=site, isactive=isactive, enhanced=enhanced)
                dbo.session.add(vlan)
                dbo.session.commit()
                flash("Added {0} in {1}".format(vlanid, site.name), category='success')
        
        if subnets and not sites:
            for subnet in subnets:
                vlan = VLAN(vlanid, subnet=subnet, site=None, isactive=isactive, enhanced=enhanced)
                dbo.session.add(vlan)
                dbo.session.commit()
                flash("Added {0} to {1}".format(vlanid, subnet.subnet), category='success')
        
        if not sites and not subnets:
            vlan = VLAN(vlanid, subnet=None, site=None, isactive=isactive, enhanced=enhanced)
            dbo.session.add(vlan)
            dbo.session.commit()
            flash("Added {}".format(vlanid), category='success')


    return redirect('/vlans')

@app.route('/vlans/edit/<int:vlanid>', methods=['GET', 'POST'])
def vlans_edit(vlanid):
    if request.method == 'GET':
        vlan = VLAN.query.filter_by(id=int(vlanid)).first()
        return render_template('vlans_edit.html', vlan=vlan)
    
    if request.method == 'POST':
        vlan = VLAN(int(request.form['vlanid']))
        dbo.session.add(vlan)
        dbo.session.commit()

    return redirect('/vlans')

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