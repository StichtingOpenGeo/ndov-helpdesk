from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^aanmelden/', include('signup.urls')),
    url(r'^wachtwoord/$', auth_views.password_change, name='auth_password_change'),
    url(r'^wachtwoord/aangepast/$', auth_views.password_change_done),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'))
]
