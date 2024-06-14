# canvas-lti-redirect-tool
This is Canvas LTI redirect tool

## Generating Django security key

`python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

## LTI install
1. Need to run this command once in order for LTI to work
```sh
 docker exec -it clrt_web /bin/bash -c \
  "python manage.py rotate_keys" 
```  
2. Create superuser via using `python maage.py createsuperuser', need to run a proxy like loophole or ngrok for LTI installation and login with that user.
https://<url>/admin/
4. Use `LTIRegistration` to configure an LTI tool

