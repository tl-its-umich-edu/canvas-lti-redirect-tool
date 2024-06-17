#!/bin/bash

# Case insensitive match
shopt -s nocaseglob

echo "$DJANGO_SETTINGS_MODULE"

echo "Waiting for DB"
while ! nc -z "${MYSQL_HOST}" "${MYSQL_PORT}"; do
  sleep 1 # wait 1 second before check again
done

echo Running python startups
python manage.py migrate
python manage.py collectstatic --verbosity 0 --noinput

echo "Starting Gunicorn"
exec gunicorn backend.wsgi:application \
    --bind 0.0.0.0:6000 \
    --workers=1 \
    --timeout=120 \
    --reload