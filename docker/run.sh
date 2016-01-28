(su proprio && cd /opt/apps/proprio && /opt/ve/proprio/bin/python manage.py migrate --noinput)
supervisord -c /opt/supervisor.conf -n
