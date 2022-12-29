from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _
from task_manager.models import User


class IndexPageView(View):

    def get(self, request):
        
        return render(request, 'index.html', context={
        'who': _('World'),
    })


class UsersListView(View):

    def get(self, request):
        users = User.objects.all()
        return render(
            request,
            'users.html',
            context={ 'users': users } 
        )