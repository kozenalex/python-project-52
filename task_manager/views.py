from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.models import MyUser
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.forms import MyUserCreationForm, MyUserUpdateForm


class IndexPageView(View):

    def get(self, request):
        
        return render(request, 'index.html', context={
        'who': _('World'),
    })


class UsersListView(ListView):

    model = MyUser
    context_object_name = 'users_list'
    template_name = 'users.html'


class UserAuthView(LoginView):

    template_name = 'login.html'

class UserLogoutView(LogoutView):
    
    reverse_lazy('index_page')


class UserCreateView(CreateView):
    form_class = MyUserCreationForm
    model = MyUser
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')


class UserUpdateView(UpdateView):
    form_class = MyUserUpdateForm
    model = MyUser
    template_name = 'user_update.html'
    success_url = reverse_lazy('users_list')


class UserDeleteView(DeleteView):
    model = MyUser
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
