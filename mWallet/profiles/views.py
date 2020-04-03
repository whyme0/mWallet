from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import Person
from .tools import create_download_files
from .forms import PersonEditForm


class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'

    # added method_decorator because it's class-based view and
    # login_required can't work without it
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        create_download_files(pk=self.request.user.pk)
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': 'Profile',
            'profile_a': 'active',
            'profile_d': 'disabled',
        })

        return ctx


class EditProfile(FormView):
    form_class = PersonEditForm
    template_name = 'profiles/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = PersonEditForm(instance=request.user)

        ctx = self.get_context_data()
        ctx['form'] = form

        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = PersonEditForm(self.request.POST, instance=self.request.user)

        ctx = self.get_context_data()
        ctx['form'] = form
        if form.is_valid():
            form.save()

            messages.success(request, 'Profile successfully changed.')
            return redirect('profiles:edit_profile')

        return render(request, self.template_name, ctx)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'title': 'Edit Profile',
            'settings_a': 'active',
            'settings_d': 'disabled',
        })

        return ctx
