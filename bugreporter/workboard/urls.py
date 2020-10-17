from django.urls import path
from . import views
from .views import ProjectListView, BugListView, BugDetailView, ProjectCreateView, BugCreateView, ProjectUpdateView, BugUpdateView, BugDeleteView, ProjectDeleteView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-home'),
    # changing this to search view
    path('project/<int:pk>/', BugListView.as_view(), name='bug-home'),
    path('project/bug/<int:pk>/',
         BugDetailView.as_view(), name='bug-detail'),
    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/bug/new/', BugCreateView.as_view(), name='bug-create'),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(), name='project-update'),
    path('project/bug/<int:pk>/update/',
         BugUpdateView.as_view(), name='bug-update'),
    path('project/bug/<int:pk>/delete/',
         BugDeleteView.as_view(), name='bug-delete'),
    path('project/<int:pk>/delete/',
         ProjectDeleteView.as_view(), name='project-delete'),
    path('project/bug/<int:pk>/comment',
         views.addComment, name='bug-detail-comment'),
    path('project/bug/comment/delete/<int:pk>/',
         views.deleteComment, name='bug-detail-comment-delete'),
    path('project/bug/comment/update/<int:pk>/',
         views.updateCommentView, name='bug-detail-comment-update-view'),
    path('project/bug/comment/update/<int:pk>/done',
         views.updateComment, name='bug-detail-comment-update'),
    path('bug/search/',
         views.bugSearch, name='bug-search'),

]
