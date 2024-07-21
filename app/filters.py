import django_filters
from app.models import Task


class TaskFilter(django_filters.FilterSet):
    # Фильтрация по статусу
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    # Сортировка по дате создания и статусу
    ordering = django_filters.OrderingFilter(fields=(
        ('created_at', 'created_at'),  # Сортировка по дате создания
        ('status', 'status')  # Сортировка по статусу
    ))

    class Meta:
        model = Task
        fields = ['status']  # Поля для фильтрации
