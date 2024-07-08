from django.urls import path

from app.views import TaskCreateView, TaskListView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('listtask/', TaskListView.as_view(), name='task_list'),

]
