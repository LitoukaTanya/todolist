from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/task/', include('app.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),    # конечная точка для входа,выхода и сброса пароля
    path('api-auth/', include('rest_framework.urls')),

]
