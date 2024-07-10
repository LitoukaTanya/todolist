from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Task, Category, Priority
from app.serializers import TaskSerializer, CategorySerializer, PrioritySerializer


# Представление для создания новой задачи
class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление для получения всех задач пользователя
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(created_by=user, deleted=False)


# Представление для получения задач пользователя по статусу
class TaskListByStatus(generics.ListAPIView):
    serializer_class = TaskSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Task.objects.filter(status=status)
        else:
            return Task.objects.none()


# Представление для получения задач пользователя по категории
class TaskListByCategory(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        category = self.kwargs['category_id']
        return Task.objects.filter(category=category)


# Представление для получения задач пользователя по приоритету
class TaskListByPriority(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        priority = self.kwargs['priority_id']
        return Task.objects.filter(priority=priority)


# Представление для получения конкретной задачи пользователя по ID
class TaskUserById(generics.RetrieveAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(created_by=user, deleted=False)


class UpdateTaskView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class DeleteTaskView(generics.RetrieveDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        # Проверяем, является ли пользователь создателем задачи
        if request.user == instance.created_by:
            instance.soft_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Проверяем, является ли пользователь администратором
        if request.user.is_staff:
            instance.hard_delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Если пользователь не создатель и не администратор, возвращаем ошибку доступа
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
