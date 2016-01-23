from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _
from signup.models import SignupQueue


class ApplyLicenseForm(forms.ModelForm):

    tech_name = forms.CharField(label=_('Name (technical contact)'))
    tech_email = forms.EmailField(label=_('Email (technical contact)'))

    class Meta:
        model = SignupQueue
        exclude = ('signed_file', 'date_requested', 'date_uploaded', 'date_verified', 'status')

    def __init__(self, *args, **kwargs):
        super(ApplyLicenseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4 col-md-6'
        self.helper.field_class = 'col-lg-6 col-md-6'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup_apply'
        self.helper.layout = Layout(
            Div(Field('organization'),
                css_class='col-md-6'),
            Div(css_class='clearfix'),
            Div(
                Div(HTML("{% load i18n %}<h4>{% trans 'Contact' %}</h4>"),
                    Field('name'),
                    Field('email'),
                    Field('position'),
                    Field('city'),
                    css_class='col-md-6'),
                Div(HTML("{% load i18n %}<h4>{% trans 'Technical contact' %}</h4>"),
                    Field('tech_name'),
                    Field('tech_email'),
                    css_class='col-md-6'),
                css_class='row'
            )


        )
        self.helper.add_input(Submit('submit', _('Apply')))

    def save(self, commit=True):
        return super(ApplyLicenseForm, self).save(commit)


class UploadSignedForm(forms.ModelForm):
    
    class Meta:
        model = SignupQueue
        fields = ['signed_file']