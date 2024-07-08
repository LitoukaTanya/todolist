from django.urls import path

from app.views import TaskCreateView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),

]
