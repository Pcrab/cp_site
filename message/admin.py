from django.contrib import admin

# Register your models here.
from message.models import MessageBase, UserMessage

admin.site.register(UserMessage)
