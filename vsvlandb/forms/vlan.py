from vsvlandb.models import Site, Subnet

from flask.ext.wtf import Form

from wtforms import TextField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

def active_sites():
	return Site.query.filter_by(isactive=True)

def active_subnets():
	return Subnet.query.filter_by(isactive=True)

class VlanForm(Form):
	# Required:
	vlan = IntegerField(u'VLAN', validators=[NumberRange(min=1,max=4096), DataRequired()])

	# Optionals
	# subnet = SelectMultipleField(u'Subnets', coerce=int, validators=[NumberRange(min=1)])
	# site = SelectMultipleField(u'Site', coerce=int)

	subnets = QuerySelectMultipleField(get_label='subnet', query_factory=active_subnets)
	sites = QuerySelectMultipleField(get_label='name', query_factory=active_sites)

	isactive = BooleanField(u'Active')
	enhanced = BooleanField(u'Enhanced')
