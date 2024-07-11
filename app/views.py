from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from app.models import Task, Category, Priority
from app.serializers import TaskSerializer, CategorySerializer, PrioritySerializer


# представление для создания задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# Представление для получения всех задач пользователя
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(created_by=user, deleted=False)


# Представление для получения всех задач по статусу
# class TaskListByStatus(generics.ListAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
#
# def get_queryset(self):
#     status = self.request.query_params.get('status')
#     if status:
#         return Task.objects.filter(status=status)
#     else:
#         return Task.objects.none()


# Представление для получения задач пользователя по категории
class TaskListByCategory(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        category = self.kwargs['pk']
        return Task.objects.filter(category=category)


# Представление для получения задач пользователя по приоритету
class TaskListByPriority(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        priority = self.kwargs['pk']
        return Task.objects.filter(priority=priority)


# Представление для получения конкретной задачи пользователя по ID
class TaskUserById(generics.RetrieveAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(created_by=user, deleted=False)


# представление для обновления конкретной задачи
class UpdateTaskView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# представление для удаление конкретной задачи
class DeleteTaskView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        if request.user == task.created_by:
            if request.user.is_staff:
                task.hard_delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                task.soft_delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


# представление для создания категории
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# представление для получения категории по ID
class GetCategoryById(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# представление для изменения категории
class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# представление для удаления конкретной категории
class DeleteCategoryView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)

        if request.user.is_staff:
            category.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            category.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# представление для создания приоритете
class PriorityCreateView(generics.CreateAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


# представление для получения приоритета по ID
class PriorityGetById(generics.RetrieveAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


# представление для изменения приоритета
class PriorityUpdateView(generics.UpdateAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


# представление для удаления конкретного приоритета
class PriorityDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        priority = get_object_or_404(Priority, pk=pk)
        if request.user.is_staff:
            priority.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            priority.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
