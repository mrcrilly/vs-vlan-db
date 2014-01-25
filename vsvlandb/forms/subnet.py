from flask.ext.wtf import Form

from wtforms import TextField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange, Length

class SubnetForm(Form):
	# Required:
	subnet = TextField(u'Subnet', validators=[DataRequired(), Length(min=1, max=50)])

	# Optionals
	site = SelectMultipleField(u'Site', coerce=int)

	isactive = BooleanField(u'Active')
	enhanced = BooleanField(u'Enhanced')
