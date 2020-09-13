from django.urls import path
from . import views
from .views import ProjectListView, BugListView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-home'),
    path('bug/', BugListView.as_view(), name='bug-home'),
]
