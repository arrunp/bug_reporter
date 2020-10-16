from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Project, Bug, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from collections import Counter

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
    paginate_by = 6
    model = Bug
    template_name = 'workboard/bug_list.html'
    context_object_name = 'bugs'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):

        bug_status = []

        for bug in Bug.objects.filter(project=Project.objects.filter(id=self.kwargs['pk']).first()):
            bug_status.append(bug.status)

        bug_status_count = Counter(bug_status)

        context = {
            'project_title': Project.objects.filter(id=self.kwargs['pk']).first().title,
            'project_summary': Project.objects.filter(id=self.kwargs['pk']).first().summary,
            'project_id': self.kwargs['pk'],
            'new_count': bug_status_count['New'],
            'onhold_count': bug_status_count['On Hold'],
            'active_count': bug_status_count['Active'],
            'resolved_count': bug_status_count['Resolved'],
            'closed_count': bug_status_count['Closed'],
            'bug_count': len(bug_status)

        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)


class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    template_name = 'workboard/bug_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'project_id': Bug.objects.filter(id=self.kwargs['pk']).first().project.id,
            'comments': reversed(Comment.objects.all()),
            'comments_length': len(Comment.objects.filter(bug=Bug.objects.filter(id=self.kwargs['pk']).first()))
        }

        kwargs.update(context)
        return super().get_context_data(**kwargs)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    # template_name = 'workboard/project_create.html'
    fields = ['title', 'summary']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    fields = ['bug_title', 'bug_type', 'status', 'severity', 'bug_summary']

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
    fields = ['bug_title', 'bug_type', 'status', 'severity', 'bug_summary']

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

    def test_func(self):
        bug = self.get_object()
        if self.request.user == bug.creator:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('bug-home', args=(self.object.project.id,))


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.creator:
            return True
        else:
            return False


def addComment(request,  **kwargs):

    context = {
        'pk': kwargs['pk']
    }

    if request.method == 'POST':
        if request.POST.get('content'):
            comment = Comment()
            comment.text = request.POST.get('content')
            comment.author = request.user
            comment.bug = Bug.objects.filter(
                id=kwargs['pk']).first()

            comment.save()

            context = {
                'pk': kwargs['pk']
            }

            return HttpResponseRedirect(reverse('bug-detail', args=(context['pk'],)))

        else:
            messages.warning(
                request, 'Please add text in the comment field to post')

            return HttpResponseRedirect(reverse('bug-detail', args=(context['pk'],)))


def updateComment(request, **kwargs):
    if request.method == 'POST':
        if request.POST.get('updateComment'):

            bug_id = Comment.objects.filter(
                id=kwargs['pk']).first().bug.id

            comment = Comment.objects.filter(id=kwargs['pk']).first()

            comment.text = "hello, update"
            comment.save()

            context = {
                'pk': bug_id
            }

            return HttpResponseRedirect(reverse('bug-detail', args=(context['pk'],)))


def deleteComment(request, **kwargs):
    if request.method == 'POST':
        if request.POST.get('deleteComment'):

            bug_id = Comment.objects.filter(
                id=kwargs['pk']).first().bug.id

            if Comment.objects.filter(id=kwargs['pk']).first().author == request.user:
                Comment.objects.filter(id=kwargs['pk']).delete()
            else:
                messages.warning(
                    request, 'You cannot delete comments that are not yours')

            context = {
                'pk': bug_id
            }

            return HttpResponseRedirect(reverse('bug-detail', args=(context['pk'],)))


'''


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = "workboard/comment_update.html"
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('bug-detail', args=(self.object.bug.id,))
'''


def bugSearch(request):
    if request.method == 'GET':
        search = request.GET.get('bugSearch')
        queryset = []
        search = search.split(" ")

        for word in search:
            found_bugs = Bug.objects.filter(
                Q(bug_title__icontains=word) | Q(
                    bug_summary__icontains=word)
            ).distinct()

            for bug in found_bugs:
                queryset.append(bug)

        return render(request, 'workboard/bug_search.html', {'found_bugs': queryset})
