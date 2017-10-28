from django.shortcuts import render


def index_view(request):
    return render(request, 'study/index.html')


def auth_view(request):
    return render(request, 'study/auth.html')