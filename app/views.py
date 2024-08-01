from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from app.form import TaskForm
from app.models import Task, Category, Priority
from django.contrib.auth.decorators import login_required
import requests


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
            messages.error(request, 'Failed to delete the task. Please try again.')


@login_required
@require_POST
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user == task.created_by or request.user.is_staff:
        completed = request.POST.get('completed') == 'true'
        task.completed = completed
        task.status = 'completed' if completed else 'pending'
        task.save()
    return redirect('task_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registrations.html', {'form': form})
