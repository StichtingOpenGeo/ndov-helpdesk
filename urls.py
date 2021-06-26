from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
import django.contrib.auth.views as auth_views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aanmelden/', include('signup.urls')),
    path('wachtwoord/', auth_views.PasswordChangeView.as_view(), name='auth_password_change'),
    path('wachtwoord/aangepast/', auth_views.PasswordChangeDoneView.as_view()),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'))
]
