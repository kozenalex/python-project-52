from django.db import models

class User(models.Model):
    login = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
