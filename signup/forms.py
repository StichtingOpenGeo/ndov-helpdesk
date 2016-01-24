from django import forms
from signup.models import SignupQueue


class ApplyLicenseForm(forms.ModelForm):
    
    class Meta:
        model = SignupQueue
        exclude = ('signed_file', 'date_requested', 'date_uploaded', 'date_verified', 'status')


class UploadSignedForm(forms.ModelForm):
    
    class Meta:
        model = SignupQueue
        fields = ['signed_file']