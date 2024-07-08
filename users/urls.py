from django.contrib import admin
from django.urls import path
from .views import user_create, UserList, UserDetail, UserUpdate, UserDeleteView

app_name = 'users'

urlpatterns = [
    path('create/', user_create, name='create'),    # создание пользователя
    path('listusers/', UserList.as_view(), name='listusers'),   # получение всех пользователей
    path('<int:pk>/', UserDetail.as_view(), name='detail'),     # получение пользователя по ID
    path('update/<int:pk>/', UserUpdate.as_view(), name='update'),       # обновление пользователя
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),      # удаление пользователя

]