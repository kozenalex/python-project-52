from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.list import ListView
from django.contrib import messages
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from task_manager.mixins import DelProtectionMixin, MyUserPermissionMixin
from users.forms import MyUserCreationForm
from users.models import MyUser


class UserView(LoginRequiredMixin, SuccessMessageMixin):

    login_url = 'login'
    model = MyUser


class UsersListView(ListView):

    model = MyUser
    context_object_name = 'users_list'
    template_name = 'users.html'


class UserCreateView(SuccessMessageMixin, CreateView):

    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'edit.html'
    success_message = _('User profile created successfully')
    extra_context = {
        'title': _('Registration'),
        'button': _('Signin')
    }
    success_url = reverse_lazy('login')


class UserUpdateView(MyUserPermissionMixin, UserView, UpdateView):

    form_class = MyUserCreationForm
    template_name = 'edit.html'
    extra_context = {
        'title': _('Update user profile'),
        'button': _('Update')
    }
    success_message = _('Profile updated')
    success_url = reverse_lazy('users_list')


class UserPassChangeView(UserView, PasswordChangeView):

    template_name = 'pass_change.html'
    success_message = _('Password changed')
    success_url = reverse_lazy('users_list')


class UserDeleteView(MyUserPermissionMixin, UserView, DeleteView, DelProtectionMixin):

    template_name = 'confirm_delete.html'
    extra_context = {
        'title': _('Delete user'),
        'is_user': True
    }
    success_message = _('User profile deleted')
    success_url = reverse_lazy('users_list')

    def post(self, request, *args, **kwargs):
        try:
            request.user.delete()
            messages.success(request, self.success_message)
        except ProtectedError:
            messages.error(request, _('You can not delete user who is in use'))
        return redirect(self.success_url)
