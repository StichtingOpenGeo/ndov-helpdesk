from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^license/', include('licensing.urls')),
	url(r'^helpdesk/', include('helpdesk.urls')),
    url(r'^password/$', 'django.contrib.auth.views.password_change', name='auth_password_change'),
    url(r'^password/done/$', 'django.contrib.auth.views.password_change_done'),
    ('^', include('django.contrib.flatpages.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
