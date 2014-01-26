from flask.ext.wtf import Form

from wtforms import TextField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange, Length

class ImpactForm(Form):
	# Required:
	name = TextField(u'Name', validators=[DataRequired(), Length(min=1, max=30)])

	# Optionals
	description = TextField(u'Description')
	isactive = BooleanField(u'Active')
