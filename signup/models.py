from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

class SignupQueue(models.Model):
    # Data for generating signup
    email = models.EmailField(unique=True)
    representative = models.CharField(_('Name of representative'), max_length=75) 
    position = models.CharField(_('Position'), max_length=100)
    business = models.CharField(_('Organization name'), max_length=100)
    city = models.CharField(_('Signing city'), max_length=50)
    
    # Uploaded signup
    signed_file = models.FileField(upload_to=settings.SIGNUP_UPLOAD_TO)

    # Track progress
    STATUSES = ((1, _('Request')),
                (2, _('Generated')),
                (3, _('Uploaded')),
                (4, _('Verified')),
                )
    status = models.IntegerField(_('Status'), default=1, choices=STATUSES)
    date_requested = models.DateField(auto_now_add=True)
    date_uploaded = models.DateField(blank=True, null=True)
    date_verified = models.DateField(blank=True, null=True)
    
    def __unicode(self):
        return u'%s - %s'  % (self.representative, self.business)