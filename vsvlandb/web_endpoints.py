
from vsvlandb import app, dbo, vlans, subnets, sites, impacts, helpers
from vsvlandb.models import VLAN, Subnet, Site, Impact, vlan_subnets
from vsvlandb.forms import vlan, subnet, site, impact

from flask import redirect, request, render_template, url_for, flash

from sqlalchemy.exc import IntegrityError

import re
import ipaddress
import sys
import inspect

from datetime import datetime
from sets import Set

from random import shuffle, randint

# Root/Index
@app.route('/')
def index():
    vlan_data = VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id)).limit(20)
    subn_data = Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id)).limit(20)

    return render_template('index.html', vlans=vlan_data, subnets=subn_data)

# VLANS
@app.route('/vlans')
def vlans_list():
    data = {
        'active': VLAN.query.filter_by(isactive=True).order_by(dbo.desc(VLAN.id)),
        'inactive': VLAN.query.filter_by(isactive=False).order_by(dbo.desc(VLAN.id))
    }

    return render_template('vlans/vlans_list.html', vlans=data)

@app.route('/vlans/add', methods=['GET', 'POST'])
def vlans_add():
    data = helpers.top_ten()
    form = vlan.VlanForm()

    if form.validate_on_submit():
        target = VLAN(form.vlan.data)
        form.populate_obj(target)

        if target.subnets:
            existing = dbo.session.query(VLAN).filter(VLAN.vlan==target.vlan,
                                                      VLAN.sites.any(Site.id.in_([i.id for i in target.sites])))
            if existing:
                clashes = existing.filter(VLAN.subnets.any(Subnet.id.in_([i.id for i in target.subnets])))
                if clashes:
                    for v in clashes.all():
                        flash("You are clashing with VLAN {0} ({1})".format(v.vlan, v.description or v.id),category='danger')
                        dbo.session.rollback()

                        return render_template('vlans/vlans_add.html', data=data, form=form)
        
        dbo.session.add(target)

        try:
            dbo.session.commit()
        except IntegrityError as e:
            dbo.session.rollback()
            flash("That VLAN already exists", category='danger')
            return render_template('vlans/vlans_add.html', data=data, form=form)
        else:
            flash("Added VLAN {}".format(target.vlan), category='success')
            return redirect('/vlans/view/{}'.format(target.id))
    else:
        helpers.flash_errors(form.errors)

    return render_template('vlans/vlans_add.html', data=data, form=form)

@app.route('/vlans/view/<int:vlanid>')
def vlans_view(vlanid):
    vlan = VLAN.query.filter_by(id=vlanid).first()
    return render_template('vlans/vlans_view.html', vlan=vlan)

@app.route('/vlans/edit/<int:vlanid>', methods=['GET', 'POST'])
def vlans_edit(vlanid):
    data = helpers.top_ten()
    target = VLAN.query.get(vlanid)
    
    if not target:
        flash("Unable to find VLAN {}".format(vlan.vlan), category='warning')
        return redirect('/vlans')

    form = vlan.VlanForm(obj=target)

    if form.validate_on_submit():
        form.populate_obj(target)

        if not dbo.session.is_modified(target):
            flash("No changes to VLAN {}".format(target.vlan), category='warning')
            dbo.session.rollback()
            return redirect('/vlans/edit/{}'.format(target.id))

        if target.subnets:
            existing = dbo.session.query(VLAN).filter(VLAN.id != target.id,
                                                      VLAN.vlan==target.vlan,
                                                      VLAN.sites.any(Site.id.in_([i.id for i in target.sites])))
            if existing:
                clashes = existing.filter(VLAN.subnets.any(Subnet.id.in_([i.id for i in target.subnets])))
                if clashes:
                    for v in clashes.all():
                        flash("You are clashing with VLAN {0} ({1})".format(v.vlan, v.description or v.id),category='danger')
                        dbo.session.rollback()
                        return redirect('/vlans/edit/{}'.format(target.id))

        dbo.session.commit()
        flash("Updated VLAN {}".format(target.vlan), category='success')
        return redirect('/vlans/view/{}'.format(target.id))
    else:
        helpers.flash_errors(form.errors)

    return render_template('vlans/vlans_edit.html', data=data, vlan=target, form=form)

@app.route('/vlans/delete/<int:vlanid>', methods=['GET', 'POST'])
def vlans_delete(vlanid):
    target = VLAN.query.get(vlanid)
    if target:
        dbo.session.delete(target)
        dbo.session.commit()
        flash("Deleted VLAN {}".format(target.vlan), category='success')
    else:
        flash("Unable to find VLAN {}".format(target.vlan), category='warning')

    return redirect('/vlans')

# Subnets
@app.route('/subnets')
def subnets_list():
    lists = {
        'active': Subnet.query.filter_by(isactive=True).order_by(dbo.desc(Subnet.id)),
        'inactive': Subnet.query.filter_by(isactive=False).order_by(dbo.desc(Subnet.id)),
    }

    return render_template('subnets/subnets_list.html', subnets=lists)

@app.route('/subnets/view/<int:subnetid>')
def subnets_view(subnetid):
    target = Subnet.query.filter_by(id=subnetid).first()
    return render_template('subnets/subnets_view.html', subnet=target)

@app.route('/subnets/add', methods=['GET', 'POST'])
def subnets_add():
    form = subnet.SubnetForm()
    data = helpers.top_ten()

    if form.validate_on_submit():
        if dbo.session.query(Subnet).filter(Subnet.subnet==form.subnet.data,
                                            Subnet.sites.any(Site.id.in_([i.id for i in form.sites.data]))).all():
            flash("That subnet already exists", category='danger')
            return render_template('subnets/subnets_add.html', data=data, form=form)

        try:
            ip = ipaddress.IPv4Network(form.subnet.data.decode())
        except ipaddress.AddressValueError as e:
            flash("Address Error: {}".format(e.message), category='danger')
        except ipaddress.NetmaskValueError as e:
            flash("Netmask Error: {}".format(e.message), category='danger')
        except ValueError as e:
            flash("Error in subnet: {}".format(e.message), category='danger')
        else:
            target = Subnet(ip)
            form.populate_obj(target)

            # Sadly, I am unable to determine how-to do this in SQL due a
            # weak understanding of SQL on my part and thus, I cannot utilise
            # SQLAlchemy's query language here. The result in this for-loop
            # craziness
            if target.vlans.count>=1:
                for v in target.vlans.all():
                    for j in target.vlans.all():
                        if v.id == j.id:
                            continue

                        if v.vlan == j.vlan:
                            site_clashes = Set([x.id for x in v.sites]) & Set([y.id for y in j.sites])
                            if len(site_clashes)>=1:
                                flash("VLAN site clash between {0} vs {1}".format(v.vlan,j.vlan), category='danger')
                                dbo.session.rollback()
                                return render_template('subnets/subnets_add.html', data=data, form=form)

            try:
                dbo.session.add(target)
                dbo.session.commit()
            except IntegrityError as e:
                flash("That subnet already exists", category='danger')
                dbo.session.rollback()
                return render_template('subnets/subnets_add.html', data=data, form=form)

            flash("Added subnet {}".format(form.subnet.data), category='success')
            return redirect('/subnets/view/{}'.format(target.id))

        return render_template('subnets/subnets_add.html', data=data, form=form)

    return render_template('subnets/subnets_add.html', data=data, form=form)

@app.route('/subnets/edit/<int:subnetid>', methods=['GET', 'POST'])
def subnets_edit(subnetid):
    target = Subnet.query.get(subnetid)
    form = subnet.SubnetForm(obj=target)

    if form.validate_on_submit():
        if dbo.session.query(Subnet).filter(Subnet.subnet==form.subnet.data,
                                            Subnet.id!=subnetid,
                                            Subnet.sites.any(Site.id.in_([i.id for i in form.sites.data]))).all():
            flash("That subnet already exists", category='danger')
            return render_template('subnets/subnets_edit.html', data=helpers.top_ten(), subnet=target, form=form)

        try:
            ip = ipaddress.IPv4Network(form.subnet.data.decode())
        except ipaddress.AddressValueError as e:
            flash(u"Error in address: {}".format(e.message), category='danger')
        except ipaddress.NetmaskValueError as e:
            flash(u"Error in netmask: {}".format(e.message), category='danger')
        except:
            flash(u"Generic error", category='danger')
        else:
            form.populate_obj(target)

            if form.vlans.data:
                for v in form.vlans.data:
                    for j in form.vlans.data:
                        if v.id == j.id:
                            continue

                        if v.vlan == j.vlan:
                            site_clashes = Set([x.id for x in v.sites]) & Set([y.id for y in j.sites])
                            if len(site_clashes)>=1:
                                flash("VLAN site clash between {0} vs {1}".format(v.vlan,j.vlan), category='danger')
                                dbo.session.rollback()
                                return render_template('subnets/subnets_edit.html', data=helpers.top_ten(), subnet=target, form=form)

            dbo.session.commit()
            flash("Edited subnet {}".format(form.subnet.data), category='success')
            return redirect('/subnets/view/{}'.format(target.id))

        return redirect('/subnets/edit/{}'.format(subnetid))

    return render_template('subnets/subnets_edit.html', data=helpers.top_ten(), subnet=target, form=form)

@app.route('/subnets/delete/<int:subnetid>')
def subnets_delete(subnetid):
    target = Subnet.query.get(subnetid)

    if target:
        dbo.session.delete(target)
        dbo.session.commit()
        flash("Deleted subnet {}".format(target.subnet), category='success')
    else:
        flash("Unable to find subnet {}".format(subnet.subnet), category='warning')

    return redirect('/subnets')


#Sites
@app.route('/sites')
def sites_list():
    lists = {
        'active': Site.query.filter_by(isactive=True).order_by(dbo.desc(Site.id)),
        'inactive': Site.query.filter_by(isactive=False).order_by(dbo.desc(Site.id)),
    }

    return render_template('sites/sites_list.html', sites=lists)

@app.route('/sites/view/<int:siteid>')
def sites_view(siteid):
    target = Site.query.filter_by(id=siteid).first()
    return render_template('sites/sites_view.html', site=target)

@app.route('/sites/add', methods=['GET', 'POST'])
def sites_add():
    form = site.SiteForm()

    if form.validate_on_submit():
        target = Site(name=form.name.data)
        form.populate_obj(target)
    
        try:
            dbo.session.add(target)
            dbo.session.commit()
        except IntegrityError as e:
            flash("That site already exists", category='danger')
            dbo.session.rollback()

            return render_template('sites/sites_add.html', data=helpers.top_ten(), form=form)

        return redirect('/sites')

    else:
        helpers.flash_errors(form.errors)

    return render_template('sites/sites_add.html', data=helpers.top_ten(), form=form)

@app.route('/sites/edit/<int:siteid>', methods=['GET', 'POST'])
def sites_edit(siteid):
    form = site.SiteForm()

    if form.validate_on_submit():
        sites.edit(form, siteid)
        return redirect('/sites/view/{}'.format(siteid))
    else:
        helpers.flash_errors(form.errors)

    data = helpers.top_ten()
    target = Site.query.filter_by(id=siteid).limit(1).first()

    form.name.data = target.name
    form.description.data = target.description
    form.isactive.data = target.isactive
    
    return render_template('sites/sites_edit.html', site=target, data=data, form=form)

@app.route('/sites/delete/<int:siteid>', methods=['GET', 'POST'])
def sites_delete(siteid):
    sites.delete_id(siteid)
    return redirect('/sites')




# Impacts
@app.route('/impacts')
def impacts_list():
    data = {
        'active': Impact.query.filter_by(isactive=True).order_by(dbo.desc(Impact.id)),
        'inactive': Impact.query.filter_by(isactive=False).order_by(dbo.desc(Impact.id))
    }

    return render_template('impacts/impacts_list.html', impacts=data)

@app.route('/impacts/add', methods=['GET', 'POST'])
def impacts_add():
    form = impact.ImpactForm()

    if form.validate_on_submit():
        impacts.add(form)
        return redirect('/impacts')
    else:
        helpers.flash_errors(form.errors)

    return render_template('impacts/impacts_add.html', data=helpers.top_ten(), form=form)

@app.route('/impacts/view/<int:impactid>')
def impacts_view(impactid):
    impact = Impact.query.filter_by(id=impactid).first()
    return render_template('impacts/impacts_view.html', impact=impact)

@app.route('/impacts/edit/<int:impactid>', methods=['GET', 'POST'])
def impacts_edit(impactid):
    form = impact.ImpactForm()

    if form.validate_on_submit():
        impacts.edit(form, impactid)
        return redirect('/impacts')
    else:
        helpers.flash_errors(form.errors)

    target = Impact.query.filter_by(id=impactid).limit(1).first()

    form.name.data = target.name
    form.description.data = target.description
    form.isactive.data = target.isactive
    
    return render_template('impacts/impacts_edit.html', impact=target, data=helpers.top_ten(), form=form)

@app.route('/impacts/delete/<int:impactid>', methods=['GET', 'POST'])
def impacts_delete(impactid):
    impacts.delete_id(impactid)
    return redirect('/vlans')

@app.route('/reports')
def reports_view():
    data = []
    data.append({'name': 'London', 'data': [i*randint(1,10) for i in range(50)]})
    data.append({'name': 'New York', 'data': [i*randint(1,10) for i in range(50)]})
    data.append({'name': 'Paris', 'data': [i*randint(1,10) for i in range(50)]})


    return render_template('reports/reports_view.html', data=data)