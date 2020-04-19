from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from .models import MailingList
from .forms import MailingListForm

# Create your views here.


class MailingListView(LoginRequiredMixin, ListView):

    template_name = 'mailing_list.html'
    context_object_name = 'mailing_list'

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)


class CreateMailingListView(LoginRequiredMixin, CreateView):
    form_class = MailingListForm
    template_name = 'mailinglist_form.html'

    def get_initial(self):
        return {'owner': self.request.id}