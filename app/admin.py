from django.contrib import admin
from .models import Category, Priority, Task

admin.site.register(Category)
admin.site.register(Priority)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status', 'completed')
