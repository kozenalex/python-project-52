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


class Task(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=700, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    executor = models.ForeignKey(MyUser, related_name='executor', on_delete=models.PROTECT)
    author = models.ForeignKey(MyUser, related_name='author', on_delete=models.PROTECT)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
