from vsvlandb.models import Site, Subnet, Impact

from flask.ext.wtf import Form

from wtforms import TextField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

def active_sites():
    return Site.query.filter_by(isactive=True)

def active_subnets():
    return Subnet.query.filter_by(isactive=True)

def active_impacts():
    return Impact.query.filter_by(isactive=True)

class VlanForm(Form):
    # Required:
    vlan = IntegerField(u'VLAN', validators=[NumberRange(min=1,max=4096), DataRequired()])

    # Optional:
    subnets = QuerySelectMultipleField(query_factory=active_subnets)
    sites = QuerySelectMultipleField(query_factory=active_sites)

    impact = QuerySelectField(query_factory=active_impacts, validators=[Optional()])

    description = TextField(u'Description', validators=[Length(min=0, max=50)])

    isactive = BooleanField(u'Active', default=True)
    enhanced = BooleanField(u'Enhanced')
