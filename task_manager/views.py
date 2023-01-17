from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.models import Label, MyUser, Status, Task
from task_manager.forms import MyUserCreationForm, TaskForm
from task_manager.mixins import MyUserPermissionMixin, UserPassesTestMixin

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

    model = MyUser
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
    extra_context = {'title': _('User')}


class UserCreateView(SuccessMessageMixin, CreateView):

    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'create.html'
    success_message = _('User profile created successfully')    
    success_url = reverse_lazy('login')


class UserUpdateView(MyUserPermissionMixin, UserView, UpdateView):

    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'update.html'
    extra_context = {'is_user': True}
    success_message = _('User profile updated')
    success_url = reverse_lazy('users_list')


class UserPassChangeView(UserView, PasswordChangeView):

    template_name = 'pass_change.html'
    success_message = _('Password changed')
    success_url = reverse_lazy('users_list')


class UserDeleteView(MyUserPermissionMixin, UserView, DeleteView):

    template_name = 'confirm_delete.html'
    success_message = _('User profile deleted')
    success_url = reverse_lazy('users_list')


class StatusView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = 'login'
    model = Status
    extra_context = {'title': _('Status')}


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


class TasksListView(LoginRequiredMixin, ListView):

    login_url = 'login'
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks_list'
    


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    login_url = 'login'
    model = Task
    form_class = TaskForm
    template_name = 'create.html'
    success_message = _('Task created')
    success_url = reverse_lazy('tasks_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = MyUser.objects.get(
                id=self.request.user.id
            )
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    login_url = 'login'
    form_class = TaskForm
    model = Task
    template_name = 'update.html'
    success_message = _('Task updated')
    success_url = reverse_lazy('tasks_list')

class TaskDeleteView(UserPassesTestMixin, DeleteView):

    model = Task
    extra_context = {'title': _('Task')}
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks_list')

    def test_func(self):
        task_id = self.get_object().id
        author = Task.objects.get(id=task_id).author
        return self.request.user.id == author.id
    
    def handle_no_permission(self):
        messages.warning(self.request, _('You have no permissions'))
        return redirect(reverse_lazy('tasks_list'))


class TaskView(LoginRequiredMixin, DetailView):

    login_url = 'login'
    model = Task
    template_name = 'task.html'


class LabelsListView(LoginRequiredMixin, ListView):

    login_url = 'login'
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels_list'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Label
    fields = ['name']
    template_name = 'create.html'
    success_message = _('Label created successfuly')
    success_url = reverse_lazy('labels_list')

class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    fields = ['name']
    model = Label
    template_name = 'update.html'
    success_message = _('Label updated successfuly')
    success_url = reverse_lazy('labels_list')


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Label
    template_name = 'confirm_delete.html'
    success_message = _('Label deleted successfuly')
    success_url = reverse_lazy('labels_list')