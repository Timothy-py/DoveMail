from django.urls import path
from .views import MailingListView, CreateMailingListView, DeleteMailingListView, MailingListDetailView, \
    SubscribeToMailingListView, ThankYouForSubscribingView

app_name = "core_app"

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('new', CreateMailingListView.as_view(), name='create_mailinglist'),
    path('<uuid:pk>/delete', DeleteMailingListView.as_view(), name='delete_mailinglist'),
    path('<uuid:pk>/manage', MailingListDetailView.as_view(), name='manage_mailinglist'),
    path('<uuid:pk>/subscribe', SubscribeToMailingListView.as_view(), name='subscribe'),
    path('<uuid:pk>/thankyou', ThankYouForSubscribingView.as_view(), name='subscriber_thankyou'),
]