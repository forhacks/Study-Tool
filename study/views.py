from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse


class IndexView(generic.TemplateView):
    template_name = 'study/index.html'


class LoginView(generic.FormView):
    template_name = 'study/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(form.request, username=data['username'], password=data['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('study:dashboard'))


class DashboardView(generic.TemplateView):
    template_name = 'study/dashboard.html'
