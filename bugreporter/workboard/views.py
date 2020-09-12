from django.shortcuts import render
from django.http import HttpResponse

projects = [
    {
        'creator': 'arrun1',
        'project_name': 'Project 1',
        'content': 'What is this project for?',
        'date_created': 'Sept 10, 2020'
    },
    {
        'creator': 'arrun2',
        'project_name': 'Project 2',
        'content': 'What is this second project for?',
        'date_created': 'Sept 12, 2020'
    }
]


def home(request):
    context = {
        'projects': projects
    }
    return render(request, 'workboard/home.html', context)
