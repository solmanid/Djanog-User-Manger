# Django
from django.shortcuts import render


# Create your views here.


def show_home(request):
    return render(request, 'base.html', {})


def show_404(request):
    return render(request, 'includes/404.html', {})
