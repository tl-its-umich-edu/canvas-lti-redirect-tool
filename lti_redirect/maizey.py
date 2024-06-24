import jwt, logging
from decouple import config
from jwt.exceptions import InvalidKeyError

logger = logging.getLogger(__name__)

class SendToMaizey():
    
    def __init__(self, lti_launch_data) -> None:
        self.lti_launch_data = lti_launch_data
        self.maizey_jwt_secret = config('MAIZEY_JWT_SECRET', default=None)
        self.lti_custom_data = self.lti_launch_data['https://purl.imsglobal.org/spec/lti/claim/custom']
    
    def get_restructured_data(self):
      course_title = self.lti_launch_data['https://purl.imsglobal.org/spec/lti/claim/context']['title']
      lis = self.lti_launch_data['https://purl.imsglobal.org/spec/lti/claim/lis']

      # Restructure the course info for Maizey needs
      restructured_data = {
      "canvas_url": self.lti_custom_data["canvas_url"],
      "course": {
          "id": self.lti_custom_data["course_id"],
          "name": course_title,
          "sis_id": lis["course_offering_sourcedid"],
          "workflow_state": self.lti_custom_data["course_status"],
          "enroll_status":self.lti_custom_data["course_enroll_status"]
      },
      "term": {
          "id": self.lti_custom_data["term_id"],
          "name": self.lti_custom_data["term_name"],
          "term_start_date": self.lti_custom_data["term_start"],
          "term_end_date": self.lti_custom_data["term_end"]
      },
      "user": {
          "id": self.lti_custom_data["user_canvas_id"],
          "login_id": self.lti_custom_data["login_id"],
          "sis_id": lis["person_sourcedid"],
          "roles": self.lti_custom_data["roles"].split(","),
          "email_address": self.lti_launch_data["email"],
          "name": self.lti_launch_data["name"],
      } ,
      "account": {
          "id": self.lti_custom_data["course_canvas_account_id"],
          "name": self.lti_custom_data["course_account_name"],
          "sis_id": self.lti_custom_data["course_sis_account_id"]
      }  
      }
      logger.info(f"Course data sending to Maizey endpoint: {restructured_data}")
      return restructured_data

    def send_to_maizey(self):
       maizey_url = None
       if not self.maizey_jwt_secret:
           logger.error("Maizey JWT secret is not configured")
       try:
        course_jwt = jwt.encode(self.get_restructured_data(), self.maizey_jwt_secret, algorithm='HS256')
        maizey_url = f"{self.lti_custom_data['redirect_url']}t2/canvaslink?token={course_jwt}"
        logger.info(f"Maizey with course JWT URL: {maizey_url}")
       except (InvalidKeyError,Exception) as e:
           logger.error(f"Error encoding course data to JWT: {e}")
       return maizey_url
