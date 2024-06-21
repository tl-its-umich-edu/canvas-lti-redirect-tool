import random, logging
import string
import django.contrib.auth
from django.conf import settings
from django.shortcuts import redirect, render
from lti_tool.views import LtiLaunchBaseView
from django.contrib.auth.models import User
from lti_redirect.maizey import SendToMaizey
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)

# Create your views here.
def get_home_template(request):
  return render(request, 'home.html')

def error(request):
    return render(request, "error.html")

def validate_custom_lti_launch_data(lti_launch):
    expected_keys = [
    "roles", "term_id", "login_id", "term_end", "course_id", "term_name", "canvas_url", 
    "term_start", "redirect_url", "course_status", "user_canvas_id", 
    "course_account_name", "course_enroll_status", "course_sis_account_id", 
    "course_canvas_account_id"]
    main_key = "https://purl.imsglobal.org/spec/lti/claim/custom"
    if main_key not in lti_launch:
        logger.error(f"LTI custom '{main_key}' variables are not configured")
        return False
    
    custom_data = lti_launch[main_key]
    missing_keys = [key for key in expected_keys if key not in custom_data]
    if missing_keys:
        logger.error(f"LTI custom variables are missing in the '{main_key}' {', '.join(missing_keys)}")
        return False
    logger.debug("All keys are present.")
    return True

def login_user_from_lti(request, launch_data):
    try:
        first_name = launch_data['given_name']
        last_name = launch_data['family_name']
        email = launch_data['email']
        username = launch_data['https://purl.imsglobal.org/spec/lti/claim/custom']['login_id']
        logger.info(f'the user {first_name} {last_name} {email} {username} launch the tool')
        user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
        logger.warn(f'user {username} never logged into the app, hence creating the user')
        password = ''.join(random.sample(string.ascii_letters, settings.RANDOM_PASSWORD_DEFAULT_LENGTH))
        user_obj = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
    except Exception as e:
        logger.error(f'error occured while getting the user info from auth_user table due to {e}')
        return False
        
        
    try: 
        django.contrib.auth.login(request, user_obj)
    except (ValueError, TypeError, Exception)  as e:
        logger.error(f'Logging user after LTI launch failed due to {e}')
        return False
    return True

class ApplicationLaunchView(LtiLaunchBaseView):
    
    # @xframe_options_exempt
    def handle_resource_launch(self, request, lti_launch):
        ...  # Required. Typically redirects the users to the appropriate page.
        launch_data = lti_launch.get_launch_data()
        if not validate_custom_lti_launch_data(launch_data):
            return redirect("error")
        if not login_user_from_lti(request, launch_data):
            return redirect("error")
        maizey_url = SendToMaizey(launch_data).send_to_maizey()
        if not maizey_url:
            return redirect("error")
        context = {
            "maizey_url": maizey_url,
        }
        return render(request, "home.html", context)

    def handle_deep_linking_launch(self, request, lti_launch):
        ...  # Optional.

    def handle_submission_review_launch(self, request, lti_launch):
        ...  # Optional.

    def handle_data_privacy_launch(self, request, lti_launch):
        ...  # Optional.
        

