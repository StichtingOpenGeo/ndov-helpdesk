from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^aanmelden/', include('signup.urls')),
	url(r'^helpdesk/', include('helpdesk.urls')),
    url(r'^wachtwoord/$', 'django.contrib.auth.views.password_change', name='auth_password_change'),
    url(r'^wachtwoord/aangepast/$', 'django.contrib.auth.views.password_change_done'),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    ('^', include('django.contrib.flatpages.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
