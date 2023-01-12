from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.models import MyUser, Status
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from task_manager.forms import MyUserCreationForm, MyUserUpdateForm
from django.contrib.messages.views import SuccessMessageMixin


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


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = MyUserCreationForm
    model = MyUser
    template_name = 'create.html'
    success_message = _('User profile created successfully')
    success_url = reverse_lazy('login')


class UserUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MyUserUpdateForm
    model = MyUser
    template_name = 'update.html'
    success_message = _('User profile updated')
    success_url = reverse_lazy('users_list')


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = MyUser
    template_name = 'confirm_delete.html'
    success_message = _('User profile deleted')
    success_url = reverse_lazy('users_list')


class StatusesListView(ListView):

    model = Status
    context_object_name = 'statuses_list'
    template_name = 'statuses.html'


class StatusCreateView(SuccessMessageMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'create.html'
    success_message = _('Status created successfuly')
    success_url = reverse_lazy('statuses_list')


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'update.html'
    success_message = _('Status updated successfuly')
    success_url = reverse_lazy('statuses_list')


class StatusDeleteView(SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_message = _('Status deleted')
    success_url = reverse_lazy('statuses_list')