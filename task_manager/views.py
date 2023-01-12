from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.models import MyUser, Status
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.forms import MyUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IndexPageView(View):

    def get(self, request):
        
        return render(request, 'index.html', context={
        'who': _('World'),
    })


class UsersListView(ListView):

    model = MyUser
    context_object_name = 'users_list'
    template_name = 'users.html'


class UserAuthView(SuccessMessageMixin, LoginView):

    template_name = 'login.html'
    success_message = _('You are logged in')
    

class UserLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)

class UserView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = 'login'
    model = MyUser


class UserCreateView(SuccessMessageMixin, CreateView):

    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'create.html'
    success_message = _('User profile created successfully')
    success_url = reverse_lazy('login')


class UserUpdateView(UserPassesTestMixin, UserView, UpdateView):

    def test_func(self):
        return self.request.user.id == self.get_object().id
    
    def handle_no_permission(self):
        messages.info(self.request, _('You have no permissions'))
        return redirect(
            reverse_lazy('users_list')
        )

    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'update.html'
    success_message = _('User profile updated')
    success_url = reverse_lazy('users_list')


class UserDeleteView(UserView, DeleteView):

    template_name = 'confirm_delete.html'
    success_message = _('User profile deleted')
    success_url = reverse_lazy('users_list')


class StatusView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = 'login'
    model = Status


class StatusesListView(StatusView, ListView):

    context_object_name = 'statuses_list'
    template_name = 'statuses.html'


class StatusCreateView(StatusView, CreateView):

    fields = ['name']
    template_name = 'create.html'
    success_message = _('Status created successfuly')
    success_url = reverse_lazy('statuses_list')


class StatusUpdateView(StatusView, UpdateView):

    fields = ['name']
    template_name = 'update.html'
    success_message = _('Status updated successfuly')
    success_url = reverse_lazy('statuses_list')


class StatusDeleteView(StatusView, DeleteView):

    template_name = 'confirm_delete.html'
    success_message = _('Status deleted')
    success_url = reverse_lazy('statuses_list')