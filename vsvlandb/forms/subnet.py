from flask.ext.wtf import Form

from wtforms import TextField, StringField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange, Length

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from vsvlandb.models import Site

def active_sites():
	return Site.query.filter_by(isactive=True)

class SubnetForm(Form):
	# Required:
	subnet = TextField(u'Subnet', validators=[DataRequired(), Length(min=1, max=50)])

	# Optionals
	sites = QuerySelectMultipleField(get_label='name', query_factory=active_sites)

	isactive = BooleanField(u'Active')