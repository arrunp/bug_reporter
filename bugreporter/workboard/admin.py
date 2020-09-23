from django.contrib import admin
from .models import Project, Bug, Task, Comment

admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(Task)
admin.site.register(Comment)
