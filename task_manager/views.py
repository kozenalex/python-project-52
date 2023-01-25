from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from users.models import MyUser


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
