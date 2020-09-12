from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
