from django.conf.urls import patterns, url
from signup.views import ApplyView

urlpatterns = patterns('', 
                       url(r'^', ApplyView.as_view(), name="signup_apply"),
                       )