from django import forms
from django.utils.translation import ugettext_lazy as _

from signup.models import SignupQueue


class ApplyLicenseForm(forms.ModelForm):

    # tech_name = forms.CharField(label=_('Name'))
    # tech_email = forms.EmailField(label=_('Email'))

    class Meta:
        model = SignupQueue
        exclude = ('signed_file', 'date_requested', 'date_uploaded', 'date_verified', 'status')


class UploadSignedForm(forms.ModelForm):

    class Meta:
        model = SignupQueue
        fields = ['signed_file']
