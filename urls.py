from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
import django.contrib.auth.views as auth_views

admin.autodiscover()

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r'', include('signup.urls')),
    path(r'^wachtwoord/$', auth_views.password_change, name='auth_password_change'),
    path(r'^wachtwoord/aangepast/$', auth_views.password_change_done),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
]
