
from vsvlandb import app, dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import redirect, request, render_template, url_for

import re

# Root/Index
@app.route('/')
def index():
	lists = {
		'vlans': VLAN.query.all(),
		'subnets': Subnet.query.all(),
		'sites': Site.query.all()
	}
	return render_template('index.html', lists=lists)

# VLANS
@app.route('/vlans')
def vlans():
	vlans = VLAN.query.all()
	return render_template('vlans_list.html', vlans=vlans)

@app.route('/vlans/add', methods=['GET', 'POST'])
def vlans_add():
	if request.method == 'GET':
		return render_template('vlans_add.html')
	else:
		vlan = VLAN(int(request.form['vlanid']))
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
	subnets = Subnet.query.all()
	return render_template('subnets_list.html', subnets=subnets)

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
	sites = Site.query.all()
	return render_template('sites_list.html', sites=sites)

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