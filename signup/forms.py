from django import forms
from django.utils.translation import gettext_lazy as _

from signup.models import SignupQueue
from django_altcha import AltchaField

class ApplyLicenseForm(forms.ModelForm):

    # tech_name = forms.CharField(label=_('Name'))
    # tech_email = forms.EmailField(label=_('Email'))

    captcha = AltchaField()

    class Meta:
        model = SignupQueue
        exclude = ('signed_file', 'date_requested', 'date_uploaded', 'date_verified', 'status')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Jan de Vries'}),
        }


class UploadSignedForm(forms.ModelForm):

    class Meta:
        model = SignupQueue
        fields = ['signed_file']
