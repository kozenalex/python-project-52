from django.db import models
from django.contrib.auth.models import User


class MyUser(User):

    def __str__(self):
        return self.get_full_name()


class Status(models.Model):

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

