from django import forms
import django_filters

from task_manager.models import Task, Labels, Status, MyUser

class TaskFilter(django_filters.FilterSet):

    def set_author(self, queryset, name, value):
        if not value:
            return self.queryset
        else:
            queryset = Task.objects.filter(
                author=self.request.user.id
            )
            return queryset

    status = django_filters.ModelChoiceFilter(
        label='Status',
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'mr-4'})
    )
    executor = django_filters.ModelChoiceFilter(
        label='Executor',
        queryset=MyUser.objects.all(),
        widget=forms.Select(attrs={'class': 'mr-4'})
    )
    labels = django_filters.ModelChoiceFilter(
        label='Labels',
        queryset=Labels.objects.all(),
        widget=forms.Select(attrs={'class': 'mr-4'})
    )
    self_tasks = django_filters.BooleanFilter(
        label='Only my tasks',
        field_name='author',
        widget=forms.CheckboxInput(),
        method='set_author'
    )

    class Meta:

        model = Task
        fields = ['status', 'executor', 'labels']
        