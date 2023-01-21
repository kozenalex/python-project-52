from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from task_manager.models import MyUser, Task
from django import forms


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email']


class TaskForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = Task

        fields = ['name', 'description', 'status', 'executor', 'labels']
