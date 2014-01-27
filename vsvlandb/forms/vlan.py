from vsvlandb.models import Site, Subnet, Impact

from flask.ext.wtf import Form

from wtforms import TextField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional

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
    subnets = QuerySelectMultipleField(get_label='subnet', query_factory=active_subnets)
    sites = QuerySelectMultipleField(get_label='name', query_factory=active_sites)

    impact = QuerySelectField(get_label='name', query_factory=active_impacts)
    # impact = SelectField(u'Impact', choices=active_impacts(), coerce=int, validators=[Optional()])

    isactive = BooleanField(u'Active', default=True)
    enhanced = BooleanField(u'Enhanced')
