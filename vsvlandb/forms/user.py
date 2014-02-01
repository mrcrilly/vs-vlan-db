from vsvlandb.models import Site, Subnet, Impact

from flask.ext.wtf import Form

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Optional, Length, Email

class UserForm_Login(Form):
    email = StringField(u'Email Address', validators=[DataRequired(), Email()])
    password = PasswordField(u'Password', validators=[DataRequired()])

class UserForm_New(Form):
    # email = dbo.Column(dbo.String(100), unique=True)
    # name = dbo.Column(dbo.String(100))
    # password = dbo.Column(dbo.String(100))
    # isactive = dbo.Column(dbo.Boolean)
    # isadmin = dbo.Column(dbo.Boolean)

    # added = dbo.Column(dbo.DateTime)
    pass