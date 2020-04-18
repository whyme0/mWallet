from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.forms import FormView
from django.core.mail import send_email
from django.urls import reverse_lazy

from . import tools
from . import forms

class HomeView(TemplateView):
    template_name = 'base/home.html'
    http_methods_names = ['get']
    extra_context = {'title': 'mWallet'}

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            super().get_context_data(**kwargs),
        )


class FeedbackView(FormView):
    form_class = forms.FeedbackForm
    template_name = ''
    extra_context = {
        'title': 'Feedback',
        'token': tools.get_random_key(),
    }

    def form_valid(self, form):
        send_email()
        messages.success('Thanks for your feedback. We will certainly consider it.')
        return redirect(reverse_lazy('feedback'))


def error_404(request, exception):
    return render(request, 'base/404.html', {'title': 'Not found'})
