#!/bin/bash -e
# http://senko.net/en/django-nginx-gunicorn/

cd /home/ubuntu/feedify
source /home/ubuntu/venv_feedify/bin/activate

export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=.

exec /home/ubuntu/venv_feedify/bin/gunicorn_django \
    --user=ubuntu \
    --group=ubuntu \
    --name=feedify-gunicorn \
    -b 0.0.0.0:8002 \
    -w 2 \
    --max-requests=5000 \
    --timeout 60 \
    --preload \
    --log-level=info \
    --log-file=/var/log/feedify/gunicorn.log \
    --pid=/var/run/gunicorn/feedify.pid
