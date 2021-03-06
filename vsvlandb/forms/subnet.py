from flask.ext.wtf import Form

from wtforms import TextField, StringField, SelectMultipleField, BooleanField, IntegerField
from wtforms.validators import DataRequired, IPAddress, NumberRange, Length

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from vsvlandb.models import Site, VLAN

def active_sites():
    return Site.query.filter_by(isactive=True)

def active_vlans():
    return VLAN.query.filter_by(isactive=True)

class SubnetForm(Form):
    # Required:
    subnet = TextField(u'Subnet', validators=[DataRequired(), Length(min=1, max=50)])

    # Optionals
    vlans = QuerySelectMultipleField(query_factory=active_vlans)
    sites = QuerySelectMultipleField(query_factory=active_sites)

    description = StringField(u'Description')
    isactive = BooleanField(u'Active')