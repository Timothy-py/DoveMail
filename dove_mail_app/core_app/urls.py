from django.urls import path
from .views import MailingListView

app_name = "core_app"

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list')
]