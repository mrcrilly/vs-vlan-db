
from vsvlandb import app, dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import redirect, request, render_template, url_for, flash

import re

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

        subnets = Subnet.query.filter_by(isactive=True)
        if subnets.count() <= 0:
            data['error']['noparents'] = True
            flash(u"No subnets defined. You can't create a VLAN without a subnet.", category='danger')
        else:
            data['subnets'] = subnets

        sites = Site.query.filter_by(isactive=True)
        if sites.count() <= 0:
            data['error']['noparents'] = True
            flash(u"No sites defined. You can't have a VLAN without a site.", category='danger')
        else:
            data['sites'] = sites

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
                flash(u"Bad VLAN ID. Please try again.", category='danger')

        if 'subnet' in request.form:
            selections = request.form.getlist('subnet')
            for selection in selections:
                if re.match(r'^[0-9]{1,}$', selection):
                    subnet = Subnet.query.filter_by(id=selection).limit(1)
                    if subnet.count() >= 1:
                        subnets.append(subnet.first())
                else:
                    data['error']['badsubnetid'] = True
                    flash(u"Bad Subnet ID. Please make your selection again.", category='danger')

        if 'site' in request.form:
            selections = request.form.getlist('site')
            for selection in selections:
                if re.match(r'^[0-9]{1,}$', selection):
                    site = Site.query.filter_by(id=selection).limit(1)
                    if site.count() >= 1:
                        sites.append(site.first())
                else:
                    data['error']['badsiteid'] = True
                    flash(u"Bad Site ID. Please make your selection again.", category='danger')   

        if 'active' in request.form:
            if re.match(r'^(on|off)$', request.form['active']):
                isactive = True
            else:
                isactive = False

        if 'enhanced' in request.form:
            print "enhanced"
            if re.match(r'^(on|off)$', request.form['enhanced']):
                enhanced = True
            else:
                enhanced = False

        for site in sites:
            for subnet in subnets:
                print "{0}: {1}: {2}".format(vlanid, subnet, site)
                vlan = VLAN(vlanid, subnet, site, isactive, enhanced)
                dbo.session.add(vlan)
                dbo.session.commit()

    return redirect('/vlans')

@app.route('/vlans/edit/<int:vlanid>', methods=['GET', 'POST'])
def vlans_edit(vlanid):
	if request.method == 'GET':
		vlan = VLAN.query.filter_by(id=int(vlanid)).first()
		return render_template('vlans_edit.html', vlan=vlan)
	
	if request.method== 'POST':
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
		return render_template('subnets_add.html')
	else:
		subnet = Subnet(request.form['subnet'])
		dbo.session.add(subnet)
		dbo.session.commit()

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