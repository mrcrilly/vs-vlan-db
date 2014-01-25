# Very Simple VLAN DB

Exactly what it says on the tin: it's a very simple VLAN database for keeping track of your VLANs. I have friends who use a spreadsheet, so something like this was of use to them.

## Warning

This application is currently very fragile. It's likely that you can break it if you try hard enough. Please keep this in mind if you begin to use this application in production.

It'a also worth noting that it has not been configured to work with anything but a SQLite(3) database, so again, it's fragile.

## Installation

If you want to brave using this application, then simply take the following steps:

1. On a Linux box (Ubuntu verified at this point), make sure you have:
 1. Python 2.7
 1. python-pip
 1. virtualenv (installed via pip)
1. Clone the repository to a directory
1. Install the requirements/dependecies
 1. pip install flask flask-wtf flask-restful flask-sqlalchemy sqlalchemy ipaddress

You have a few choices at this point. You can either just './run.py', and get a locally running version (the database will be in /tmp/vlan.db), or you can install and configure NginX and uwsgi. Please see [[http://flask.pocoo.org/docs/deploying/uwsgi/|the Flask docs]] for how-to do this.

## Features

A lot is missing right now, but at present you can:

1. Add sites, such as data centres or geographical locations ("London", "Paris", etc) to organise things a bit;
1. Add subnets which can then be added to VLANs;
1. Add VLANs, which can be given a subnet (or set of) or a single/set of sites

As such the organisation of these elements is more in the DB and in the form of statistics until I write some views to display more detailed information.

