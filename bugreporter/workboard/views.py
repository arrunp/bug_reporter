from django.shortcuts import render
from .models import Project, Bug
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

'''
@login_required
def home(request):
    context = {
        'projects': Project.objects.all(),
        'title': 'Projects'
    }
    return render(request, 'workboard/home.html', context)
'''


class ProjectListView(LoginRequiredMixin, ListView):
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


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'workboard/bug_list.html'
    context_object_name = 'bugs'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = {
            'project_title': Project.objects.filter(id=self.kwargs['pk']).first().title,
            'project_summary': Project.objects.filter(id=self.kwargs['pk']).first().summary,
            'project_id': self.kwargs['pk']
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)


class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    template_name = 'workboard/bug_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'project_id': Bug.objects.filter(id=self.kwargs['pk']).first().project.id
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    #template_name = 'workboard/project_create.html'
    fields = ['title', 'summary']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    fields = ['bug_title', 'bug_summary']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.project = Project.objects.filter(
            id=self.kwargs['pk']).first()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = "workboard/project_update.html"
    fields = ['title', 'summary']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.creator:
            return True
        else:
            return False


class BugUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bug
    template_name = "workboard/bug_update.html"
    fields = ['bug_title', 'bug_summary']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bug = self.get_object()
        if self.request.user == bug.creator:
            return True
        else:
            return False


class BugDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bug
    success_url = '/'

    def test_func(self):
        bug = self.get_object()
        if self.request.user == bug.creator:
            return True
        else:
            return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.creator:
            return True
        else:
            return False
