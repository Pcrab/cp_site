from django.db import models


# Create your models here.
from users.models import User


class MessageBase(models.Model):
    from_user: models.CharField(max_length=20)
    content: models.CharField()
    send_time: models.DateTimeField()
    reply_to: models.CharField(default="")

    def is_valid(self):
        try:
            if self.reply_to != "":
                self.objects.get(id=self.reply_to)
            User.objects.get(username=self.from_user)
        except models.DoesNotExist as e:
            return False
        if self.content:
            return True

    class Meta:
        abstract = True


class UserMessage(MessageBase):
    to_user: models.CharField(max_length=20)
