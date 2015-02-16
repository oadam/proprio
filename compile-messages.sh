#!/bin/bash
# a simple script to compile messages from our projects
APPS=$(python -c "from proprio import settings;print ' '.join(settings.INSTALLED_APPS)")
for APP in $APPS; do
	if [ -d $APP ] # process our directories and skip imported apps
		then
			(cd $APP && django-admin compilemessages)
	fi
done
