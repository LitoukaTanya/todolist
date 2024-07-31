from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


from app.views import task_list, task_detail, task_update, task_delete, update_task_status
from users.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/task/', include('app.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),    # Включение всех путей dj_rest_auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

]
urlpatterns += [
    path('', task_list, name='task_list'),
    path('task/<int:pk>/', task_detail, name='task_detail'),
    path('task/update/<int:pk>/', task_update, name='update_task'),
    path('task/delete/<int:pk>/', task_delete, name='delete_task'),
    path('task/<int:pk>/status/', update_task_status, name='update_task_status')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)