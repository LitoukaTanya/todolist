from django.urls import path

from app.views import TaskCreateView, TaskListView, TaskListByStatus, TaskListByCategory, TaskListByPriority

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('listtask/', TaskListView.as_view(), name='task_list'),
    path('listtask/status/', TaskListByStatus.as_view(), name='task_status'),
    path('listtask/category/<int:category_id>/', TaskListByCategory.as_view(), name='task_category'),
    path('listtask/priority/<int:priority_id>/', TaskListByPriority.as_view(), name='task_priority'),

]
