from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import MailingList

# Create your views here.


class MailingListView(LoginRequiredMixin, ListView):

    template_name = 'mailing_list.html'
    context_object_name = 'mailing_list'

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)