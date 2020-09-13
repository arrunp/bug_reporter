from django.urls import path
from . import views
from .views import ProjectListView, BugListView, BugDetailView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-home'),
    path('project/<int:pk>/bugs/', BugListView.as_view(), name='bug-home'),
    path('project/bugs/<int:pk>/',
         BugDetailView.as_view(), name='bug-detail'),

]
