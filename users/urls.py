from django.contrib import admin
from django.urls import path
from .views import user_create, UserList

app_name = 'users'

urlpatterns = [
    path('create/', user_create, name='create'),
    path('listusers/', UserList.as_view(), name='listusers',)

]