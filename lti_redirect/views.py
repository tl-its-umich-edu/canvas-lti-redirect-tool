import requests
import jwt
from django.shortcuts import redirect, render
from lti_tool.views import LtiLaunchBaseView

# Create your views here.
def get_home_template(request):
  return render(request, 'home.html')

def get_restrucutured_data(launch_data):
    print('you are in get_restructured_data')
    # print(launch_data)
    custom = launch_data['https://purl.imsglobal.org/spec/lti/claim/custom']
    course_title = launch_data['https://purl.imsglobal.org/spec/lti/claim/context']['title']
    lis = launch_data['https://purl.imsglobal.org/spec/lti/claim/lis']
    # Restructure the data as per the requirements
    restructured_data = {
    "canvas_url": custom["canvas_url"],
    "course": {
        "id": custom["course_id"],
        "name": course_title,
        "sis_id": lis["course_offering_sourcedid"],
        "workflow_state": custom["course_status"],
        "enroll_status":custom["course_enroll_status"]
    },
    "term": {
        "id": custom["term_id"],
        "name": custom["term_name"],
        "term_start_date": custom["term_start"],
        "term_end_date": custom["term_end"]
    },
    "user": {
        "id": custom["user_canvas_id"],
        "login_id": custom["login_id"],
        "sis_id": lis["person_sourcedid"],
        "roles": custom["roles"].split(","),
        "email_address": launch_data["email"],
        "name": launch_data["name"],
    } ,
    "account": {
        "id": custom["course_canvas_account_id"],
        "name": custom["course_account_name"],
        "sis_id": custom["course_sis_account_id"]
    }  
    }
    print(restructured_data)
    return restructured_data



class ApplicationLaunchView(LtiLaunchBaseView):
    
    # @xframe_options_exempt
    def handle_resource_launch(self, request, lti_launch):
        ...  # Required. Typically redirects the users to the appropriate page.
        print('you are in LTI launch')
        launch_data = lti_launch.get_launch_data()
        custom = launch_data['https://purl.imsglobal.org/spec/lti/claim/custom']
        redirect_url = custom['redirect_url']
        print(custom)
        return redirect("home")

    def handle_deep_linking_launch(self, request, lti_launch):
        ...  # Optional.

    def handle_submission_review_launch(self, request, lti_launch):
        ...  # Optional.

    def handle_data_privacy_launch(self, request, lti_launch):
        ...  # Optional.
        

