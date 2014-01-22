
from vsvlandb import app

from flask import request, render_template

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/vlans')
def vlans():
	return render_template('vlans.html')

@app.route('/sites')
def sites():
	return render_template('sites.html')