from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index_view(request):
    return render(request, 'study/index.html')


def auth_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('study:dashboard'))
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'study/auth.html', context)


def dashboard_view(request):
    return render(request, 'study/dashboard.html')
