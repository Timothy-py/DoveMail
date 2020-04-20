from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy

from .mixins import UserCanUseMailingList
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


class DeleteMailingListView(LoginRequiredMixin, UserCanUseMailingList, DeleteView):
    model = MailingList
    success_url = reverse_lazy('core_app:mailing_list')


class MailingListDetailView(LoginRequiredMixin, UserCanUseMailingList, DetailView):
    model = MailingList
    template_name = 'mailinglist_detail.html'