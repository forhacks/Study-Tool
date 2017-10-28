from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse

from .models import Deck
from .forms import DeckForm


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
            return HttpResponseRedirect(reverse('study:dashboard:index'))


class LogoutView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse('study:index')


class DashboardView(generic.TemplateView):
    template_name = 'study/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['user_decks'] = Deck.objects.filter(owner=self.request.user)
        return context


class NewDeckView(generic.FormView):
    template_name = 'study/new_deck.html'
    form_class = DeckForm

    def form_valid(self, form):
        deck = form.save(commit=False)
        deck.owner = self.request.user
        deck.save()
        return HttpResponseRedirect(reverse('study:dashboard:index'))

    def get_context_data(self, **kwargs):
        context = super(NewDeckView, self).get_context_data(**kwargs)
        context['user_decks'] = Deck.objects.filter(owner=self.request.user)
        return context


class DeckView(generic.DetailView):
    template_name = 'study/deck.html'
    model = Deck

    def get_context_data(self, **kwargs):
        context = super(DeckView, self).get_context_data(**kwargs)
        context['user_decks'] = Deck.objects.filter(owner=self.request.user)
        return context
