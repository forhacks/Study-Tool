from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Deck, Card
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


class SignUpView(generic.FormView):
    template_name = 'study/signup.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()

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


class CreateDeckView(generic.CreateView):
    template_name = 'study/new_deck.html'
    form_class = DeckForm

    def form_valid(self, form):
        deck = form.save(commit=False)
        deck.owner = self.request.user
        deck.save()
        return HttpResponseRedirect(reverse('study:dashboard:deck:index', args=(deck.id,)))

    def get_context_data(self, **kwargs):
        context = super(CreateDeckView, self).get_context_data(**kwargs)
        context['user_decks'] = Deck.objects.filter(owner=self.request.user)
        return context


class DeckView(generic.DetailView):
    template_name = 'study/deck.html'
    model = Deck

    def get_context_data(self, **kwargs):
        context = super(DeckView, self).get_context_data(**kwargs)
        context['user_decks'] = Deck.objects.filter(owner=self.request.user)
        return context


class UpdateDeckView(generic.UpdateView):
    template_name = 'study/edit_deck.html'
    form_class = DeckForm
    model = Deck

    def form_valid(self, form):
        deck = form.save()
        return HttpResponseRedirect(reverse('study:dashboard:deck:index', args=(deck.id,)))

    def get_context_data(self, **kwargs):
        context = super(UpdateDeckView, self).get_context_data(**kwargs)
        context['user_decks'] = Deck.objects.filter(owner=self.request.user)
        return context


def update_deck_view(request, pk):
    deck = get_object_or_404(Deck, pk=pk)

    CardInlineFormSet = inlineformset_factory(Deck, Card, fields=('term', 'definition'))

    if request.method == "POST":
        formset = CardInlineFormSet(request.POST, instance=deck)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('study:dashboard:deck:index', args=(deck.id,)))
    else:
        formset = CardInlineFormSet(instance=deck)
        print('test')

    context = {
        'formset': formset,
        'deck': deck,
        'user_decks': Deck.objects.filter(owner=request.user)
    }

    return render(request, 'study/edit_deck.html', context)
