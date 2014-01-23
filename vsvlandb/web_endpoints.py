
from vsvlandb import app

from flask import request, render_template

# Root/Index
@app.route('/')
def index():
	return render_template('index.html')



# VLANS
@app.route('/vlans')
def vlans():
	return render_template('vlans_list.html')

@app.route('/vlans/add')
def vlans_add():
	return render_template('vlans_add.html')

@app.route('/vlans/edit')
def vlans_edit():
	return render_template('vlans_edit.html')

@app.route('/vlans/delete')
def vlans_delete():
	return render_template('vlans_delete.html')



# Subnets
@app.route('/subnets')
def subnets():
	return render_template('subnets_list.html')

@app.route('/subnets/add')
def subnets_add():
	return render_template('subnets_add.html')

@app.route('/subnets/edit')
def subnets_edit():
	return render_template('subnets_edit.html')

@app.route('/subnets/delete')
def subnets_delete():
	return render_template('subnets_delete.html')



#Sites
@app.route('/sites')
def sites():
	return render_template('sites_list.html')

@app.route('/sites/add')
def sites_add():
	return render_template('sites_add.html')

@app.route('/sites/edit')
def sites_edit():
	return render_template('sites_edit.html')

@app.route('/sites/delete')
def sites_delete():
	return render_template('sites_delete.html')