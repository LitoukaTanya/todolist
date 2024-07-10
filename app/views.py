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
    permission_classes = [IsAuthenticated]

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


class CategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCategoryById(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DeleteCategoryView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user.is_staff:
            category.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            category.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PriorityCreateView(generics.CreateAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class PriorityGetById(generics.RetrieveAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class PriorityUpdateView(generics.UpdateAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class PriorityDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            priority = Priority.objects.get(pk=pk)
        except Priority.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user.is_staff:
            priority.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            priority.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
