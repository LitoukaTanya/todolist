# from django.contrib.sites import requests
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from app.form import TaskForm
from app.models import Task, Category, Priority
from app.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from app.serializers import TaskReadSerializer, TaskWriteSerializer, CategorySerializer, PrioritySerializer
from django.contrib.auth.decorators import login_required
import requests


# представление для создания задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TaskWriteSerializer
        return TaskReadSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Представление для получения всех задач
class TaskListView(generics.ListAPIView):
    serializer_class = TaskReadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.filter(deleted=False)
        return Task.objects.filter(created_by=user, deleted=False)


# Представление для получения всех задач по статусу
# class TaskListByStatus(generics.ListAPIView):
#     serializer_class = TaskSerializer

# def get_queryset(self):
#     status = self.request.query_params.get('status')
#     if status:
#         return Task.objects.filter(status=status)
#     else:
#         return Task.objects.none()


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


@login_required
def task_list(request):
    token = request.user.auth_token.key  # Получаем токен пользователя
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('http://localhost:8000/api/task/listtask/', headers=headers)
    tasks = response.json() if response.status_code == 200 else []
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'category': form.cleaned_data['category'].id,
                'priority': form.cleaned_data['priority'].id,
                'status': form.cleaned_data['status'],
                'created_by': request.user.id
            }
            create_task_response = requests.post('http://localhost:8000/api/task/create/', headers=headers, json=data)
            if create_task_response.status_code == status.HTTP_201_CREATED:
                return redirect('task_list')
    else:
        form = TaskForm()

    categories = Category.objects.filter(deleted=False)
    priorities = Priority.objects.filter(deleted=False)

    return render(request, 'app/task_list.html', {
        'tasks': tasks,
        'form': form,
        'categories': categories,
        'priorities': priorities
    })


@login_required
def task_detail(request, pk):
    token = request.user.auth_token.key
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(f'http://localhost:8000/api/task/{pk}/', headers=headers)
    task = response.json() if response.status_code == 200 else None

    return render(request, 'app/task_detail.html', {'task': task})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                form.save()
                return redirect('task_detail', pk=pk)
            except Exception as e:
                form.add_error(None, str(e))
        else:
            form.add_error(None, 'Please correct the errors below.')
    else:
        form = TaskForm(instance=task)

    return render(request, 'app/task_update.html', {'form': form, 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        token = request.user.auth_token.key
        headers = {
            'Authorization': f'Token {token}'
        }
        response = requests.delete(f'http://localhost:8000/api/task/delete/{pk}/', headers=headers)
        if response.status_code == 204:
            return redirect('task_list')
        else:
            return redirect('task_detail', pk=pk)
    else:
        return redirect('task_detail', pk=pk)
