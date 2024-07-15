from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from app.views import task_list, task_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/task/', include('app.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),    # конечная точка для входа,выхода и сброса пароля
    path('api-auth/', include('rest_framework.urls')),

]
urlpatterns += [
    path('', task_list, name='task_list'),
    path('task/<int:pk>/', task_detail, name='task_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)