from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('signup.urls')),
    url(r'^wachtwoord/$', 'django.contrib.auth.views.password_change', name='auth_password_change'),
    url(r'^wachtwoord/aangepast/$', 'django.contrib.auth.views.password_change_done'),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
)
