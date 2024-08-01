# from rest_framework import serializers
# from app.models import Task, Category, Priority


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'
#
#
# class PrioritySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Priority
#         fields = '__all__'
#
#
# # Сериализатор для чтения данных модели Task
# class TaskReadSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)   # Вложенный сериализатор для Category
#     priority = PrioritySerializer(read_only=True)   # Вложенный сериализатор для Priority
#     status_display = serializers.SerializerMethodField()    # Дополнительное поле для отображения статуса
#
#     class Meta:
#         model = Task
#         fields = ('id', 'title', 'description', 'status', 'completed', 'created_at', 'completed_at', 'updated_at',
#                   'deleted_at', 'deleted', 'created_by', 'category', 'priority', 'status_display')
#
#     # Метод для получения текстового отображения статуса
#     def get_status_display(self, obj):
#         return obj.get_status_display()
#
#
# # Сериализатор для записи данных модели Task
# class TaskWriteSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Поле для выбора категории
#     priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())  # Поле для выбора приоритета
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Task
#         fields = ('id', 'title', 'description', 'status', 'completed', 'created_at', 'completed_at', 'updated_at',
#                   'deleted_at', 'deleted', 'created_by', 'category', 'priority')
