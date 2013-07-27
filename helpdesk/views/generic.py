from django.views.generic import TemplateView

class TemplateContextView(TemplateView):
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(TemplateContextView, self).get_context_data(**kwargs)
        if self.extra_context is not None:
          context.update(self.extra_context)
        return context