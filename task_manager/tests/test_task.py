from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import MyUser, Labels, Task, Status


class TestTask(TestCase):

    def setUp(self) -> None:
        MyUser.objects.create_user(username='alex_alexov', password='qwerty')
        Labels.objects.create(name='test')
        Status.objects.create(name='test')
        self.c = Client()
        self.c.post(
            reverse('login'),
            data={'username': 'alex_alexov', 'password': 'qwerty'}
        )
        self.user = MyUser.objects.get(id=1)
        self.label = Labels.objects.get(id=1)
        self.status = Status.objects.get(id=1)
        self.task = Task.objects.create(
            name='test',
            description='test',
            status=self.status,
            executor=self.user,
            author=self.user
        )
        self.task.labels.add(self.label)

    def test_task_create(self):
        response = self.c.post(
            reverse('task_create'),
            data={
                'name': 'test2',
                'description': 'test2',
                'status': 1,
                'executor': 1,
                'author': 1,
                'labels': 1
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertEqual(Task.objects.all().count(), 2)

    def test_task_update(self):
        response = self.c.post(
            reverse('task_update', kwargs={'pk': 1}),
            data={
                'name': 'test1',
                'description': 'test2',
                'status': 1,
                'executor': 1,
                'author': 1,
                'labels': 1
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTemplateUsed(response, 'tasks.html')

    def test_task_read(self):
        response = self.c.get(
            reverse('task_view', kwargs={'pk': 1}),
            content_type='text/html'
        )
        self.assertTemplateUsed(response, 'task.html')
        self.assertContains(response, self.task.name)

    def test_task_delete(self):
        response = self.c.post(
            reverse('task_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTemplateUsed(response, 'tasks.html')
