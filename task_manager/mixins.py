from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _


class MyUserPermissionMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.id == self.get_object().id
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, _('You have no permissions'))
            return redirect(
                reverse_lazy('users_list')
            )
        else:
            messages.warning(self.request, _('You must log in'))
            return redirect(
                reverse_lazy('login')
            )
