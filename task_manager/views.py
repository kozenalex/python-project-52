from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.filter import TaskFilter
from task_manager.models import Labels, MyUser, Status, Task
from task_manager.forms import TaskForm
from task_manager.mixins import DelProtectionMixin, UserPassesTestMixin


class IndexPageView(View):

    def get(self, request):

        return render(request, 'index.html', context={'who': _('World')})


class UserAuthView(SuccessMessageMixin, LoginView):

    model = MyUser
    template_name = 'login.html'
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class StatusView(LoginRequiredMixin, SuccessMessageMixin):
    login_url = 'login'
    model = Status


class StatusesListView(StatusView, ListView):

    context_object_name = 'statuses_list'
    template_name = 'statuses.html'
    extra_context = {'title': _('Status')}


class StatusCreateView(StatusView, CreateView):

    fields = ['name']
    template_name = 'edit.html'
    success_message = _('Status created successfuly')
    success_url = reverse_lazy('statuses_list')
    extra_context = {
        'title': _('Create status'),
        'button': _('Create')
    }


class StatusUpdateView(StatusView, UpdateView):

    fields = ['name']
    template_name = 'edit.html'
    extra_context = {
        'title': _('Update status'),
        'button': _('Update')
    }
    success_message = _('Status updated successfuly')
    success_url = reverse_lazy('statuses_list')


class StatusDeleteView(DelProtectionMixin, StatusView, DeleteView):

    template_name = 'confirm_delete.html'
    extra_context = {
        'title': _('Delete status')
    }
    success_message = _('Status deleted')
    success_url = reverse_lazy('statuses_list')


class TasksListView(LoginRequiredMixin, FilterView):

    login_url = 'login'
    model = Task
    template_name = 'tasks.html'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    login_url = 'login'
    model = Task
    form_class = TaskForm
    template_name = 'edit.html'
    extra_context = {
        'title': _('Create task'),
        'button': _('Create')
    }
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
    template_name = 'edit.html'
    extra_context = {
        'title': _('Update task'),
        'button': _('Update')
    }
    success_message = _('Task updated')
    success_url = reverse_lazy('tasks_list')


class TaskDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):

    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Successfull task deleteion')
    extra_context = {
        'title': _('Delete task')
    }

    def test_func(self):
        task_id = self.get_object().id
        author = Task.objects.get(id=task_id).author
        return self.request.user.id == author.id

    def handle_no_permission(self):
        messages.warning(self.request, _('Only author can delete task'))
        return redirect(reverse_lazy('tasks_list'))


class TaskView(LoginRequiredMixin, DetailView):

    login_url = 'login'
    model = Task
    template_name = 'task.html'


class LabelsListView(LoginRequiredMixin, ListView):

    login_url = 'login'
    model = Labels
    template_name = 'labels.html'
    context_object_name = 'labels_list'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Labels
    fields = ['name']
    template_name = 'edit.html'
    extra_context = {
        'title': _('Create label'),
        'button': _('Create')
    }
    success_message = _('Label created successfuly')
    success_url = reverse_lazy('labels_list')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    fields = ['name']
    model = Labels
    template_name = 'edit.html'
    extra_context = {
        'title': _('Update label'),
        'button': _('Update')
    }
    success_message = _('Label updated successfuly')
    success_url = reverse_lazy('labels_list')


class LabelDeleteView(LoginRequiredMixin, DelProtectionMixin, SuccessMessageMixin, DeleteView):

    model = Labels
    template_name = 'confirm_delete.html'
    extra_context = {
        'title': _('Delete label')
    }
    success_message = _('Label deleted successfuly')
    success_url = reverse_lazy('labels_list')
