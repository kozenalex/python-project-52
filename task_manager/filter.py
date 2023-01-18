from django import forms
from django_filters import filters, filterset
from task_manager.models import Task, Labels, Status, MyUser


class TaskFilter(filterset.FilterSet):

    def set_author(self, queryset, name, value):
        if not value:
            return queryset
        else:
            return queryset.filter(author=self.request.user.id)
        

    status = filters.ModelChoiceFilter(
        label='Status',
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'mr-4'})
    )
    executor = filters.ModelChoiceFilter(
        label='Executor',
        queryset=MyUser.objects.all(),
        widget=forms.Select(attrs={'class': 'mr-4'})
    )
    labels = filters.ModelChoiceFilter(
        label='Labels',
        queryset=Labels.objects.all(),
        widget=forms.Select(attrs={'class': 'mr-4'})
    )
    self_tasks = filters.BooleanFilter(
        label='Only my tasks',
        field_name='author',
        widget=forms.CheckboxInput(),
        method='set_author'
    )

    class Meta:

        model = Task
        fields = ['status', 'executor', 'labels']
