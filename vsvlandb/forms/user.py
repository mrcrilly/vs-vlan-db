from vsvlandb import dbo
from vsvlandb.models import Site, Subnet, Impact

from flask.ext.wtf import Form

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Optional, Length, Email

class UserForm_Login(Form):
    email = StringField(u'Email Address', validators=[DataRequired(), Email()])
    password = PasswordField(u'Password', validators=[DataRequired()])

class UserForm_New(Form):
    email = StringField(u'Email Address', validators=[DataRequired(), Email()])
    name = StringField(u'Name', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Password', validators=[DataRequired()])

    isactive = BooleanField(u'Active User', default=True)
    isadmin = BooleanField(u'Administrator', default=False)
    isreadonly = BooleanField(u'Read Only', default=False)
    canapi = BooleanField(u'API Access', default=False)

    added = dbo.Column(dbo.DateTime)
    lastlogin = dbo.Column(dbo.DateTime)