from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from signup.views import ApplyView

urlpatterns = patterns('', 
                       url(r'^bedankt/$', TemplateView.as_view(template_name="signup/signupqueue_thanks.html"), name="signup_step2"),
                       url(r'^$', ApplyView.as_view(), name="signup_apply")
                       )