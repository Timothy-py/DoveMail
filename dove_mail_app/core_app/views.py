from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied

from .mixins import UserCanUseMailingList
from .models import MailingList, Subscriber
from .forms import MailingListForm, SubscriberForm, MessageForm

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


class SubscribeToMailingListView(CreateView):
    form_class = SubscriberForm
    template_name = 'subscriber_form.html'

    def get_initial(self):
        return {'mailing_list': self.kwargs['mailinglist_id']}

    def get_success_url(self):
        return reverse('core_app:subscriber_thankyou', kwargs={'pk': self.object.mailing_list.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_list_id = self.kwargs['mailinglist_id']
        context['mailing_list'] = get_object_or_404(MailingList, id=mailing_list_id)
        return context


class ThankYouForSubscribingView(DetailView):
    model = MailingList
    template_name = 'subscription_thankyou.html'


class ConfirmSubscriptionView(DetailView):
    model = Subscriber
    template_name = 'confirm_subscription.html'

    def get_object(self, queryset=None):
        subscriber = super().get_object(queryset=queryset)
        subscriber.confirmed = True
        subscriber.save()
        return subscriber


class UnsubscribeView(DeleteView):
    model = Subscriber
    template_name = 'unsubscribe.html'

    def get_success_url(self):
        mailing_list = self.object.mailing_list
        return reverse('core_app:subscribe', kwargs={'mailinglist_pk': mailing_list.id})


class CreateMessageView(LoginRequiredMixin, CreateView):
    SAVE_ACTION = 'save'
    PREVIEW_ACTION = 'preview'

    form_class = MessageForm
    template_name = 'message_form.html'

    def get_success_url(self):
        return reverse('core_app:manage_mailinglist', kwargs={'pk': self.object.mailing_list.id})

    def get_initial(self):
        mailing_list = self.get_mailing_list()
        return {'mailing_list': mailing_list.id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailing_list = self.get_mailing_list()
        context.update({
            'mailing_list': mailing_list,
            'SAVE_ACTION': self.SAVE_ACTION,
            'PREVIEW_ACTION': self.PREVIEW_ACTION
        })
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == self.PREVIEW_ACTION:
            context = self.get_context_data(
                form=form,
                message=form.instance
            )
            return self.render_to_response(context=context)
        elif action == self.SAVE_ACTION:
            return super().form_valid(form)

    def get_mailing_list(self):
        mailing_list = get_object_or_404(MailingList, id=self.kwargs['mailinglist_pk'])
        if not mailing_list.user_can_use_mailing_list(self.request.user):
            raise PermissionDenied()
        return mailing_list