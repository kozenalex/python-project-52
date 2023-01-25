from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django_filters.views import FilterView
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.filter import TaskFilter
from task.models import Task
from users.models import MyUser
from task.forms import TaskForm
from task_manager.mixins import UserPassesTestMixin


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
