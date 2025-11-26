# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from signup.models import SignupQueue
from signup.forms import ApplyLicenseForm, UploadSignedForm


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

class ApplyView(CreateView):
    form_class = ApplyLicenseForm
    model = SignupQueue
    template_name = 'signup/signupqueue_form.html'

    def get_success_url(self):
        return reverse_lazy('signup_step2')

    def form_valid(self, form):
        # form.send_email()
        self.object = form.save()
        return HttpResponse('<script>window.location.href="' + self.get_success_url() + '";</script>')

    def add_name_validation_js(self, html, request):
        # Add JavaScript validation using the template
        js_code = render_to_string('signup/name_validator_js.html', request=request)

        # Insert the JavaScript before the closing head tag
        return html.replace('</head>', js_code + '</head>')

    def get(self, request, *args, **kwargs):
        # Get the form
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Render the template
        context = self.get_context_data(form=form)
        html = render_to_string(self.template_name, context, request=request)

        # Add JavaScript validation and return
        html = self.add_name_validation_js(html, request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        # Handle form submission
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            # Render the template with form errors
            context = self.get_context_data(form=form)
            html = render_to_string(self.template_name, context, request=request)

            # Add JavaScript validation and return
            html = self.add_name_validation_js(html, request)
            return HttpResponse(html)


class UploadView(UpdateView):
    form_class = UploadSignedForm
    model = SignupQueue

    def get_success_url(self):
        return reverse_lazy('signup_step3')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        return super(UploadView, self).form_valid(form)
