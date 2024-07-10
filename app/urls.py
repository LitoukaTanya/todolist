from django.urls import path

from app.views import TaskCreateView, TaskListView, TaskListByStatus, TaskListByCategory, TaskListByPriority, \
    TaskUserById, UpdateTaskView, DeleteTaskView, CategoryCreateView, GetCategoryById, UpdateCategoryView, \
    DeleteCategoryView, PriorityCreateView, PriorityGetById

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('listtask/', TaskListView.as_view(), name='task_list'),
    path('listtask/status/', TaskListByStatus.as_view(), name='task_status'),
    path('listtask/category/<int:category_id>/', TaskListByCategory.as_view(), name='task_category'),
    path('listtask/priority/<int:priority_id>/', TaskListByPriority.as_view(), name='task_priority'),
    path('<int:pk>/', TaskUserById.as_view(), name='task_id'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='task_update'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='task_delete'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/', GetCategoryById.as_view(), name='category_get'),
    path('category/update/<int:pk>/', UpdateCategoryView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', DeleteCategoryView.as_view(), name='category_delete'),
    path('priority/create/', PriorityCreateView.as_view(), name='task_priority_create'),
    path('priority/<int:pk>/', PriorityGetById.as_view(), name='task_priority_get'),

]
