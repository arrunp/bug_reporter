from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-home')


class Bug(models.Model):
    New = 'New'
    Active = 'Active'
    OnHold = 'On Hold'
    Resolved = 'Resolved'
    Closed = 'Closed'

    Bug = 'Bug'
    Task = 'Task'

    STATUS_CHOICES = [
        (New, 'New'),
        (Active, 'Active'),
        (OnHold, 'On Hold'),
        (Resolved, 'Resolved'),
        (Closed, 'Closed')
    ]

    BUG_TYPE_CHOICES = [
        (Bug, 'Bug'),
        (Task, 'Task')
    ]

    bug_title = models.CharField(max_length=150)
    bug_summary = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=New)
    bug_type = models.CharField(
        max_length=4, choices=BUG_TYPE_CHOICES, default=Bug)

    def __str__(self):
        return self.bug_title

    def get_absolute_url(self):
        return reverse('bug-detail', kwargs={'pk': self.pk})


class Task(models.Model):
    New = 'New'
    Active = 'Active'
    OnHold = 'On Hold'
    Resolved = 'Resolved'
    Closed = 'Closed'

    STATUS_CHOICES = [
        (New, 'New'),
        (Active, 'Active'),
        (OnHold, 'On Hold'),
        (Resolved, 'Resolved'),
        (Closed, 'Closed')
    ]

    task_title = models.CharField(max_length=150)
    task_summary = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=New)

    def __str__(self):
        return self.task_title


class Comment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
