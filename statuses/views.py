from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from statuses.models import Status
from task_manager.mixins import DelProtectionMixin


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
