from django.test import TestCase, Client
from task_manager.models import MyUser


class TestMyUser(TestCase):

    def setUp(self) -> None:

        MyUser.objects.create(username='alex_alexov', password='qwerty')