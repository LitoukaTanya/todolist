from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.http import require_POST

from app.filters import TaskFilter
from app.form import TaskForm
from app.models import Task, Category, Priority
from app.permissions import IsOwnerOrAdmin
from api.serializers import TaskReadSerializer, TaskWriteSerializer, CategorySerializer, PrioritySerializer
from django.contrib.auth.decorators import login_required
import requests

from app.permissions import IsAdminOrReadOnly, IsProfileOwnerOrAdmin
from .serializers import UserSerializer, UserSoftDeleteSerializer


# представление для создания пользователя
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# представление для получения всех пользователей
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# представление для получения пользователя по ID
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileOwnerOrAdmin]


# представление для изменения пользователя
class UserUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileOwnerOrAdmin]


# представление для удаления пользователя
class UserDeleteView(APIView):

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if request.user.is_staff:
            user.delete()  # Жесткое удаление
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.user == user:
            serializer = UserSoftDeleteSerializer(user, data={'is_active': False}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TaskWriteSerializer
        return TaskReadSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Автоматическое назначение пользователя, создавшего задачу


# Представление для получения всех задач
class TaskListView(generics.ListAPIView):
    serializer_class = TaskReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.filter(deleted=False)  # Все задачи для админов
        return Task.objects.filter(created_by=user, deleted=False)  # Задачи только текущего пользователя


class TaskListByStatus(generics.ListAPIView):
    serializer_class = TaskReadSerializer

    def get_queryset(self):

        status_param = self.request.query_params.get('status')  # Получаем статус из параметров запроса
        if status_param is None:
            return Task.objects.none()  # Если статус не передан, возвращаем пустой QuerySet

        user = self.request.user
        if user.is_staff:
            # Если пользователь администратор, возвращаем все задачи с указанным статусом
            return Task.objects.filter(status=status_param, deleted=False)
        else:
            # Если обычный пользователь, возвращаем только его задачи с указанным статусом
            return Task.objects.filter(created_by=user, status=status_param, deleted=False)


# Представление для получения задач по категории
class TaskListByCategory(generics.ListAPIView):
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        category_id = self.kwargs['pk']  # Получаем id категории из URL
        user = self.request.user
        if user.is_staff:
            return Task.objects.filter(category_id=category_id, deleted=False)
        return Task.objects.filter(category_id=category_id, created_by=user, deleted=False)


# Представление для получения задач по приоритету
class TaskListByPriority(generics.ListAPIView):
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        priority_id = self.kwargs['pk']
        user = self.request.user
        if user.is_staff:
            return Task.objects.filter(priority_id=priority_id, deleted=False)
        return Task.objects.filter(priority_id=priority_id, created_by=user, deleted=False)


# Представление для получения конкретной задачи пользователя по ID
class TaskUserById(generics.RetrieveAPIView):
    serializer_class = TaskReadSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Task.objects.filter(deleted=False)


# представление для обновления конкретной задачи
class UpdateTaskView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskWriteSerializer
        return TaskReadSerializer


# представление для удаление конкретной задачи
class DeleteTaskView(APIView):

    def delete(self, request, pk, *args, **kwargs):
        """

        """
        task = get_object_or_404(Task, pk=pk)
        if request.user == task.created_by or request.user.is_staff:
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
    permission_classes = [IsAdminOrReadOnly]


# представление для изменения категории
class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


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
    permission_classes = [IsAdminOrReadOnly]


# представление для изменения приоритета
class PriorityUpdateView(generics.UpdateAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsAdminOrReadOnly]


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
