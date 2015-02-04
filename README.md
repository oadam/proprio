property-management
===================
[![Build Status](https://drone.io/github.com/oadam/proprio/status.png)](https://drone.io/github.com/oadam/proprio/latest)

A free as in a beer property management software to manage your tenants

Installation
------------
`pip install -r requirements.txt`
`python manage.py syncdb`
`python manage.py runserver`

Custom bank file parser
-----------------------
To register a new bank format parser, duplicate the existing bank format parser, modifiy its methods, and add it to the list of importers specified by the `PROPRIO_IMPORT_PARSERS` property in django settings

Run with Docker
---------------
This app can be run using Docker. It will put its sqlite db and its uploaded files into a /data volume that you have to provide.
It also expects a `SECRET_KEY` environment variable.
