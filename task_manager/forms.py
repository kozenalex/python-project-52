from task_manager.models import Task
from django import forms


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = ['name', 'description', 'status', 'executor', 'labels']
