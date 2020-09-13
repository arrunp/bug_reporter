from django.shortcuts import render
from .models import Project, Bug
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

'''
@login_required
def home(request):
    context = {
        'projects': Project.objects.all(),
        'title': 'Projects'
    }
    return render(request, 'workboard/home.html', context)
'''


class ProjectListView(ListView):
    model = Project
    template_name = 'workboard/home.html'
    context_object_name = 'projects'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Projects'
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)


class BugListView(ListView):
    model = Bug
    template_name = 'workboard/bug.html'
    context_object_name = 'bugs'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = {
            'project_id': self.kwargs['pk']
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)
