
from vsvlandb import app, dbo
from vsvlandb.models import VLAN, Subnet, Site

from flask import redirect, request, render_template, url_for

# Root/Index
@app.route('/')
def index():
	return render_template('index.html')



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
		print "Got POST"

		vlan = VLAN(request.form['vlanId'])
		dbo.session.add(vlan)
		dbo.session.commit()

		return redirect(url_for('/vlans'))

@app.route('/vlans/edit/<int:vlanid>')
def vlans_edit(vlanid):
	return render_template('vlans_edit.html')

@app.route('/vlans/delete/<int:vlanid>')
def vlans_delete(vlanid):
	return render_template('vlans_delete.html')


# Subnets
@app.route('/subnets')
def subnets():
	return render_template('subnets_list.html')

@app.route('/subnets/add')
def subnets_add():
	return render_template('subnets_add.html')

@app.route('/subnets/edit/<int:subnetid>')
def subnets_edit(subnetid):
	return render_template('subnets_edit.html')

@app.route('/subnets/delete/<int:subnetid>')
def subnets_delete(subnetid):
	return render_template('subnets_delete.html')



#Sites
@app.route('/sites')
def sites():
	return render_template('sites_list.html')

@app.route('/sites/add')
def sites_add():
	return render_template('sites_add.html')

@app.route('/sites/edit/<int:siteid>')
def sites_edit(siteid):
	return render_template('sites_edit.html')

@app.route('/sites/delete/<int:siteid>')
def sites_delete(siteid):
	return render_template('sites_delete.html')