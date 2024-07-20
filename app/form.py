from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority', 'status', 'category', 'completed')
        widgets = {
            'completed': forms.CheckboxInput()
        }