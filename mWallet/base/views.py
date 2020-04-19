from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages

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
    template_name = 'base/feedback.html'
    extra_context = {
        'title': 'Feedback',
        'token': tools.get_random_key(),
    }

    def form_valid(self, form):
        tools.send_yandex_email(
            form.cleaned_data['email'],
            form.cleaned_data['feedback_title'],
            form.cleaned_data['feedback_message'],
        )
        messages.success(self.request, 'Thanks for your feedback. We will certainly consider it.')
        return redirect(reverse_lazy('feedback'))


def error_404(request, exception):
    return render(request, 'base/404.html', {'title': 'Not found'})
