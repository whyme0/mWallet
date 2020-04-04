from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


def log_out(request):
    logout(request)

    messages.success(request, 'You\'re successfully loged out.')
    return redirect('home')
