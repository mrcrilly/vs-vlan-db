
from vsvlandb import app

from flask import request, render_template

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/vlans')
def vlans():
	return render_template('vlans_list.html')

@app.route('/vlans/add')
def vlans_add():
	return render_template('vlans_add.html')

@app.route('/subnets')
def subnets():
	return render_template('subnets_list.html')

@app.route('/subnets/add')
def subnets_add():
	return render_template('subnets_add.html')

@app.route('/sites')
def sites():
	return render_template('sites_list.html')

@app.route('/sites/add')
def sites_add():
	return render_template('sites_add.html')