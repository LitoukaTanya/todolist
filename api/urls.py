from django.urls import path
from .views import UserList, UserDetail, UserUpdate, UserDeleteView, UserCreateAPIView
from api.views import TaskCreateView, TaskListView, TaskListByCategory, TaskListByPriority, \
    TaskUserById, UpdateTaskView, DeleteTaskView, CategoryCreateView, GetCategoryById, UpdateCategoryView, \
    DeleteCategoryView, PriorityCreateView, PriorityGetById, PriorityUpdateView, PriorityDeleteView, TaskListByStatus

app_name = 'api'

urlpatterns = [
    path('users/create/', UserCreateAPIView.as_view(), name='create'),  # создание пользователя
    path('users/listusers/', UserList.as_view(), name='listusers'),  # получение всех пользователей
    path('users/<int:pk>/', UserDetail.as_view(), name='detail'),  # получение пользователя по ID
    path('users/update/<int:pk>/', UserUpdate.as_view(), name='update'),  # обновление пользователя
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),  # удаление пользователя
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/listtask/', TaskListView.as_view(), name='task_list'),
    path('task/listtask/status/', TaskListByStatus.as_view(), name='task_status'),
    path('task/listtask/category/<int:pk>/', TaskListByCategory.as_view(), name='task_category'),
    path('task/listtask/priority/<int:pk>/', TaskListByPriority.as_view(), name='task_priority'),
    path('task/<int:pk>/', TaskUserById.as_view(), name='task_id'),
    path('task/update/<int:pk>/', UpdateTaskView.as_view(), name='task_update'),
    path('task/delete/<int:pk>/', DeleteTaskView.as_view(), name='task_delete'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/', GetCategoryById.as_view(), name='category_get'),
    path('category/update/<int:pk>/', UpdateCategoryView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', DeleteCategoryView.as_view(), name='category_delete'),
    path('priority/create/', PriorityCreateView.as_view(), name='task_priority_create'),
    path('priority/<int:pk>/', PriorityGetById.as_view(), name='task_priority_get'),
    path('priority/update/<int:pk>/', PriorityUpdateView.as_view(), name='task_priority_update'),
    path('priority/delete/<int:pk>/', PriorityDeleteView.as_view(), name='priority_delete'),
]
