#!/bin/bash

# Case insensitive match
shopt -s nocaseglob

echo "$DJANGO_SETTINGS_MODULE"

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=4
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=6000
fi

if [ -z "${GUNICORN_TIMEOUT}" ]; then
    GUNICORN_TIMEOUT=120
fi


echo "Waiting for DB"
while ! nc -z "${MYSQL_HOST}" "${MYSQL_PORT}"; do
  sleep 1 # wait 1 second before check again
done

echo Running python startups
python manage.py migrate

if [ "$DEBUGPY_ENABLE" = "True" ]; then
      echo "Starting Gunicorn for DEBUGPY debugging"
      # Workers need to be set to 1 for DEBUGPY
      GUNICORN_WORKERS=1
      GUNICORN_RELOAD="--reload"
      GUNICORN_TIMEOUT=0
else
      echo "Starting Gunicorn for Production"
      GUNICORN_RELOAD=
fi
echo Running Gunicorn: Workers - ${GUNICORN_WORKERS}, Port - ${GUNICORN_PORT}, Timeout - ${GUNICORN_TIMEOUT}, Reload - ${GUNICORN_RELOAD}

exec gunicorn backend.wsgi:application \
    --bind 0.0.0.0:${GUNICORN_PORT} \
    --workers="${GUNICORN_WORKERS}" \
    --timeout="${GUNICORN_TIMEOUT}" \
    ${GUNICORN_RELOAD}