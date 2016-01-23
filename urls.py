from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('signup.urls')),
    (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
)
