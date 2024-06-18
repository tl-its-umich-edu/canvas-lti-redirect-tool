# canvas-lti-redirect-tool
This is Canvas LTI redirect tool which use the CAI developed [LTI library](https://pypi.org/project/django-lti/)

### Prerequisites

To follow the instructions below, you will at minimum need the following:
1. **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**.
1. **[Git](https://git-scm.com/downloads)**
### Installation and Setup
1. You need to web Proxy like Loophole or ngrok to run the application. Loophole offers custom domain
    ```sh
    loophole http 6000 --hostname <your-host>
    ```
1. Copy the `.env.sample` file as `.env`. 
    ```sh
    cp .env.sample .env
1. Examine the `.env` file. It will have the suggested default environment variable settings,
mostly just MySQL information as well as locations of other configuration files.

1. Start the Docker build process (this will take some time).
    ```sh
    docker compose build
    ```

1. Start up the web server and database containers.
    ```sh
    docker compose up
    ```

1. generate Django secret using below command
```sh
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## LTI install
1. Need to run this command once docker container is up in order for LTI to work. This is important step otherwise the LTI tool launch won't happen
```sh
 docker exec -it clrt_web /bin/bash -c \
  "python manage.py rotate_keys" 
```
2. use the `setup/lti-config.json` for registing the LTI tool. Replace all the `{app-hostname}` with your web proxy url.  
3. Create superuser via using `python manage.py createsuperuser', need to run a proxy like loophole or ngrok for LTI installation and login with that user. Go to https://{app-hostname}/admin/. 
4. Goto `LTIRegistration` to configure an LTI tool from admin console. This will create the `uuid` automatically. Hold on to that value and update the `OpenID Connect Initiation Url` in the LTI tool registration from Canvas with this id. 
   ` for Eg: https://clrt-local.loophole.site/init/0b54a91b-cac6-4c96-ba1e/`
5. Configure the LTI configuration from CLRT tool going to admin again. Give the following value. Note: `<canvas-instance>: ['canvas.test', 'canvas.beta']`
      1. Name: any name
      2. Issuer: https://<canvas-instance>.instructure.com
      2. Client ID: (get this from Platform)
      3. Auth URL: https://<canvas-instance>.instructure.com/api/lti/authorize_redirect
      4. Access token URL: https://<canvas-instance>.instructure.com/login/oauth2/token
      5. Keyset URL: https://<canvas-instance>.instructure.com/api/lti/security/jwks
      6. DEPLOYMENT ID: get this as it is described the step 7 and paste 
6. Save
7. Go to the Canvas(platform) add the LTI tool at account/course level and copy the deployment id by clicking the setting button next to it.

## Make a user superuser
1. go to the `auth_user` table and set `is_superuser` and `is_staff` to `1` or `true` this will give the logged user access to admin interface



