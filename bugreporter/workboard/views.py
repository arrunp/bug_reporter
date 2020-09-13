from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {
        'projects': Project.objects.all(),
        'title': 'Projects'
    }
    return render(request, 'workboard/home.html', context)
