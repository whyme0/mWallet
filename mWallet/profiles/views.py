from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404

from accounts.models import Person, Wallet
from .tools import create_download_files
from .forms import PersonEditForm, WalletCreationForm, WalletEditForm


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


class PersonDeleteConfirmation(TemplateView):
    template_name = 'profiles/delete_confirmation.html'
    extra_context = {'title': 'Deleting'}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PersonDelete(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        user_pk = self.request.user.pk

        logout(self.request)
        Person.objects.get(pk=user_pk).delete()
        messages.success(self.request, 'Your Account successfully deleted.')
        return super().get_redirect_url(*args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class WalletsView(ListView):
    model = Wallet
    template_name = 'profiles/wallets.html'
    paginate_by = 5
    order_by = ['-created_date']
    extra_context = {
        'title': 'My wallets',
        'wallets_a': 'active',
        'wallets_d': 'disabled',
    }

    def get_queryset(self):
        return Wallet.objects.filter(owner=self.request.user)

    def get_context_object_name(self, obj):
        return 'wallets'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class WalletCreationView(CreateView):
    form_class = WalletCreationForm
    template_name = 'profiles/wallet-creation.html'
    success_url = reverse_lazy('profiles:profile_wallets')
    extra_context = {'title': 'Wallet creation'}

    def form_valid(self, form):
        Wallet.objects.create(owner=self.request.user, **form.cleaned_data)

        messages.success(self.request, 'Wallet "%s" successfully created.' % form.cleaned_data['name'])
        return redirect(self.success_url)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class WalletEditView(UpdateView):
    template_name = 'profiles/wallet-edit.html'
    form_class = WalletEditForm
    extra_context = {'title': 'Edit Wallet'}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Wallet successfully updated.')
        return reverse_lazy('profiles:wallet_edit', kwargs=self.kwargs)

    def get_queryset(self):
        _queryset = Wallet.objects.filter(pk=self.kwargs['pk'])

        if self.request.user == _queryset.get().owner:
            return _queryset

        raise Http404('There is no page you are looking for')


class WalletDelete(DeleteView):
    template_name = 'profiles/wallet-deletion.html'
    extra_context = {'title': 'Wallet deletion'}
    success_url = reverse_lazy('profiles:profile_wallets')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Your wallet successfully deleted.')
        return super().get_success_url()

    def get_queryset(self):
        _queryset = Wallet.objects.filter(pk=self.kwargs['pk'])

        if self.request.user == _queryset.get().owner:
            return _queryset

        raise Http404('There is no page you are looking for')

class WalletInfoView(TemplateView):
    pass
