from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from labels.models import Labels
from task_manager.mixins import DelProtectionMixin


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
