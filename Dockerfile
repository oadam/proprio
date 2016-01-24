# heavily based on https://github.com/kencochrane/django-docker/blob/master/Dockerfile
FROM ubuntu:12.04

# Set the locale (if not cannot download utf-8 file names)
# based on http://jaredmarkell.com/docker-and-locales/
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt-get -qq update
RUN apt-get install -y python-pip supervisor python-dev libpcre3-dev gettext
RUN pip install virtualenv && pip install uwsgi && pip install supervisor-stdout
RUN virtualenv --no-site-packages /opt/ve/proprio
ADD docker/supervisor.conf /opt/supervisor.conf
ADD docker/run.sh /usr/local/bin/run
ADD requirements.txt /tmp/proprio-requirements.txt
RUN /opt/ve/proprio/bin/pip install -r /tmp/proprio-requirements.txt
ADD . /opt/apps/proprio
RUN (cd /opt/apps/proprio && /opt/ve/proprio/bin/python manage.py collectstatic --noinput)
RUN (cd /opt/apps/proprio && . /opt/ve/proprio/bin/activate && ./compile-messages.sh)
# add additional_settings last because it prevents manage.py from running
ADD docker/additional_settings.py /opt/apps/proprio/additional_settings.py
RUN adduser --gecos 'user to run the app' --system proprio
EXPOSE 8000
VOLUME /data
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]
