from django.test import TestCase
from task_manager.models import Task, Status, Labels, MyUser


class TestModels(TestCase):

    def setUp(self):

        self.user = MyUser.objects.create_user(username='alex_alexov', password='qwerty')
        self.label = Labels.objects.create(name='testl')
        self.status = Status.objects.create(name='test_st')
        self.task = Task.objects.create(
            name='TestTask',
            description='testetstet',
            executor=self.user,
            author=self.user,
            status=self.status
        )

    def test_verbose_label(self):

        verbose = self.label._meta.get_field('name').verbose_name
        self.assertEqual(verbose, 'Имя')

    def test_verbose_status(self):

        verbose = self.status._meta.get_field('name').verbose_name
        self.assertEqual(verbose, 'Имя')
