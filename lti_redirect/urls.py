from django.urls import path
from . import views
from lti_tool.views import jwks, OIDCLoginInitView
from lti_redirect.views import ApplicationLaunchView
urlpatterns = [
     path('', views.get_home_template, name = 'home'),
     path('error', views.error, name="error" ),

     # LTI launch urls
    path(".well-known/jwks.json", jwks, name="jwks"),
    path("init/<uuid:registration_uuid>/", OIDCLoginInitView.as_view(), name="init"),
    path("ltilaunch", ApplicationLaunchView.as_view(), name="ltilaunch"),
]