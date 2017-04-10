from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings


class SignupQueue(models.Model):
    # Data for generating signup
    email = models.EmailField(_('Email address'), unique=True)
    name = models.CharField(_('Name (representative)'), max_length=75) 
    position = models.CharField(_('Position'), max_length=100, blank=True)
    organization = models.CharField(_('Organization name'), max_length=100, blank=True)
    city = models.CharField(_('City'), max_length=50)
    
    # Uploaded signup
    signed_file = models.FileField(upload_to=getattr(settings, 'SIGNUP_UPLOAD_TO', settings.MEDIA_ROOT), blank=True)

    # Track progress
    STATUSES = ((1, _('Request')),
                (2, _('Generated')),
                (3, _('Uploaded')),
                (4, _('Verified')),
                (5, _('Error')),
                (11, _('Migrated')),
                (12, _('Unsubscribed')),
                )
    status = models.IntegerField(_('Status'), default=1, choices=STATUSES)
    date_requested = models.DateField(auto_now_add=True)
    date_uploaded = models.DateField(blank=True, null=True)
    date_verified = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = _("registration")
    
    def __unicode__(self):
        return u'%s - %s'  % (self.name, self.organization)