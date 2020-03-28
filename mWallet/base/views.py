from django.shortcuts import render
from django.views.generic import TemplateView


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
