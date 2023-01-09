from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from task_manager.models import MyUser


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email']


class MyUserUpdateForm(UserChangeForm):

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email']
        