from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


def home(request):
    context = {
        'projects': Project.objects.all(),
        'title': 'Projects'
    }
    return render(request, 'workboard/home.html', context)
