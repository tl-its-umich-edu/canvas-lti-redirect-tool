# canvas-lti-redirect-tool
This is Canvas LTI redirect tool

## Generating Django security key

`python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
