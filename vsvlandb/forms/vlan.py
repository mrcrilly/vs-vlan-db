from flask.ext.wtf import Form

from wtforms import TextField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired

class VlanForm(Form):
	# Required:
	vlanid = TextField(u'VLAN', validators=[DataRequired()])

	# Optionals
	subnet = SelectMultipleField(u'Subnets')
	site = SelectMultipleField(u'Site')

	isactive = BooleanField(u'Active')
	enhanced = BooleanField(u'Enhanced')
