echo Running python startups
python manage.py migrate
python manage.py collectstatic --verbosity 0 --noinput

echo "Starting Gunicorn"
exec gunicorn backend.wsgi:application \
    --bind 0.0.0.0:6000 \
    --workers=1 \
    --timeout=120 \
    --reload