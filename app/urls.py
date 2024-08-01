from django.urls import path

from app.views import task_detail, task_update, task_delete, update_task_status

urlpatterns = [
    path('<int:pk>/', task_detail, name='task_detail'),
    path('update/<int:pk>/', task_update, name='update_task'),
    path('delete/<int:pk>/', task_delete, name='delete_task'),
    path('<int:pk>/status/', update_task_status, name='update_task_status')

]