from django.contrib import admin
from .models import MailingList, Subscriber, Message

# Register your models here.

admin.site.register(Message)
admin.site.register(MailingList)
admin.site.register(Subscriber)
