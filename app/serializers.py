from rest_framework import serializers

from app.models import Task, Category, Priority


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'


class TaskReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    priority = PrioritySerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'completed', 'created_at', 'completed_at', 'updated_at',
                  'deleted_at', 'deleted', 'created_by', 'category', 'priority')


class TaskWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'completed', 'created_at', 'completed_at', 'updated_at',
                  'deleted_at', 'deleted', 'created_by', 'category', 'priority')