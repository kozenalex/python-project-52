from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _


class IndexPageView(View):

    def get(self, request):
        
        return render(request, 'index.html', context={
        'who': _('World'),
    })