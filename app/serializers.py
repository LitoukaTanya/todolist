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


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    priority = PrioritySerializer()

    class Meta:
        model = Task
        fields = '__all__'
