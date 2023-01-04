from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView
from task_manager.models import MyUser
from django.views.generic.edit import CreateView
from task_manager.forms import MyUserCreationForm


class IndexPageView(View):

    def get(self, request):
        
        return render(request, 'index.html', context={
        'who': _('World'),
    })


class UsersListView(View):

    def get(self, request):
        users = MyUser.objects.all()
        return render(
            request,
            'users.html',
            context={ 'users': users } 
        )


class UserAuthView(LoginView):

    template_name = 'login.html'


class UserCreateView(CreateView):
    form_class = MyUserCreationForm
    model = MyUser
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')