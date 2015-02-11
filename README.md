property-management
===================
<span class="badges">
[![Build Status](https://drone.io/github.com/oadam/proprio/status.png)][drone]
[![Dependency Status](https://gemnasium.com/oadam/proprio.png)][gemnasium]
</span>

[drone]: https://drone.io/github.com/oadam/proprio/latest
[gemnasium]: https://gemnasium.com/oadam/proprio

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
This app can be run using Docker.

You can pull it at [oadam/proprio](https://registry.hub.docker.com/u/oadam/proprio/).

It will put its sqlite db and its uploaded files into a `/data` volume that you have to provide.
It also expects a `SECRET_KEY` environment variable containing a django secret key.
You can set the `DEBUG` variable to run django in debug mode.

You can run it on port 80 using the following 2 steps :

    docker run oadam/proprio # this will crash and generate a SECRET_KEY
    docker run --env SECRET_KEY='[the generated key]' -p 80:8000 -ti -v  /path/to/your/data/dir:/data oadam/proprio
