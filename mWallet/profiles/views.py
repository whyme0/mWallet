from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.shortcuts import render


class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'

    # added method_decorator because it's class-based view and
    # login_required can't work without it
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': 'Profile',
            'profile_a': 'active',
            'profile_d': 'disabled',
        })

        return ctx
