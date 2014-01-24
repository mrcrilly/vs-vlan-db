from flask.ext.wtf import Form

from wtforms import TextField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange

class VlanForm(Form):
	# Required:
	vlanid = IntegerField(u'VLAN', validators=[NumberRange(min=1,max=4096), DataRequired()])

	# Optionals
	subnet = SelectMultipleField(u'Subnets', coerce=int, validators=[NumberRange(min=1)])
	site = SelectMultipleField(u'Site', coerce=int, validators=[NumberRange(min=1)])

	isactive = BooleanField(u'Active')
	enhanced = BooleanField(u'Enhanced')
