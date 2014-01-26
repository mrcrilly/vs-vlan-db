
from vsvlandb import dbo
from vsvlandb.helpers import sitesAndSubnets
from vsvlandb.models import Impact

from flask import flash

def delete_id(impact_id, flash_msg=True):
	impact = Impact.query.filter_by(id=impact_id).limit(1).first()

	if impact:
		dbo.session.delete(impact)
		dbo.session.commit()

		if flash_msg:
			flash("Deleted Impact {}".format(impact.name), category='success')

def delete_impact(impact, flash_msg=True):
	impacts = Impact.query.filter_by(name=impact.name).all()

	if impacts:
		for impact in impacts:
			dbo.session.delete(impact)
			dbo.session.commit()

		if flash_msg:
			flash("Deleted Impact {}".format(impact.name), category='success')

def edit(form, impact_id, flash_msg=True):
	delete_id(impact_id, False)
	add(form, False)

	if flash_msg:
		flash("Updated Impact {0}".format(form.name.data), category='success')

def add(form, flash_msg=True):
	impact = Impact(name=form.name.data, description=form.description.data, isactive=form.isactive.data)
	dbo.session.add(impact)
	dbo.session.commit()

	if flash_msg:
		flash("Added Impact {0}".format(form.name.data), category='success')


