from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404

from accounts.models import Person, Wallet, Operation
from .tools import create_download_files
from . import forms


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
    form_class = forms.PersonEditForm
    template_name = 'profiles/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = forms.PersonEditForm(instance=request.user)

        ctx = self.get_context_data()
        ctx['form'] = form

        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = forms.PersonEditForm(self.request.POST, instance=self.request.user)

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
    """
    This class show all wallets of current person
    """
    model = Wallet
    template_name = 'profiles/wallets.html'
    paginate_by = 3
    extra_context = {
        'title': 'My wallets',
        'wallets_a': 'active',
        'wallets_d': 'disabled',
    }

    def get_queryset(self):
        return Wallet.objects.filter(
            owner=self.request.user
        ).order_by('created_date')

    def get_context_object_name(self, obj):
        return 'wallets'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class WalletCreationView(CreateView):
    form_class = forms.WalletCreationForm
    template_name = 'profiles/wallet-creation.html'
    success_url = reverse_lazy('profiles:profile_wallets')
    extra_context = {'title': 'Wallet creation'}

    def form_valid(self, form):
        Wallet.objects.create(owner=self.request.user, **form.cleaned_data)

        messages.success(
            self.request,
            'Wallet "%s" successfully created.' % form.cleaned_data['name']
        )
        return redirect(self.success_url)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class WalletEditView(UpdateView):
    template_name = 'profiles/wallet-edit.html'
    form_class = forms.WalletEditForm
    extra_context = {'title': 'Edit Wallet'}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Wallet successfully updated.')
        return reverse_lazy('profiles:current_wallet', kwargs=self.kwargs)

    def get_queryset(self):
        _queryset = Wallet.objects.filter(pk=self.kwargs['pk'])

        # if user have access to this wallet
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

        # if user have access to this wallet
        if self.request.user == _queryset.get().owner:
            return _queryset

        raise Http404('There is no page you are looking for')


class WalletInfoView(ListView):
    """
    This class shows detail info about wallet,
    but it inherit ListView instead DetailView because
    we need to show all operations of this wallet
    with pagination, order, and other shit, so we
    user ListView for WalletInfoView
    """
    template_name = 'profiles/current-wallet.html'
    context_object_name = 'operations'
    paginate_by = 5

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        wallet = Wallet.objects.get(pk=self.kwargs['pk'])
        _queryset = Operation.objects.filter(wallet=wallet).order_by('-date')

        # if user have access to this wallet
        if self.request.user == wallet.owner:
            return _queryset

        raise Http404('There is no page you are looking for')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Wallet info'
        ctx['wallet'] = Wallet.objects.get(pk=self.kwargs['pk'])

        return ctx


class OperationCreateView(CreateView):
    form_class = forms.OperationCreateForm
    template_name = 'profiles/operation-create.html'
    extra_context = {'title': 'Create operation'}

    def form_valid(self, form):
        wallet = Wallet.objects.get(pk=self.kwargs['pk'])
        if self.request.user == wallet.owner:
            Operation.objects.create(**form.cleaned_data)
            messages.success(self.request, 'The operation was successfull')

            return redirect(self.get_success_url())

        raise Http404('There is no page you are looking for')

    def get_success_url(self):
        return reverse_lazy('profiles:current_wallet', kwargs=self.kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        wallet = Wallet.objects.filter(pk=self.kwargs['pk'])
        return {'wallet': wallet}
