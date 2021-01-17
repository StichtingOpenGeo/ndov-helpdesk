from django.urls import path
from django.views.generic import TemplateView
from signup.views import ApplyView

urlpatterns = [
    path('bedankt/', TemplateView.as_view(template_name="signup/signupqueue_thanks.html"), name="signup_step2"),
    path('', ApplyView.as_view(), name="signup_apply")
]
