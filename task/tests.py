from django.test import TestCase, Client
from django.urls import reverse
from users.models import MyUser
from statuses.models import Status
from labels.models import Labels
from task.models import Task


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

    def task_filter_test(self):
        status3 = Status.objects.create(name='test3')
        Task.objects.create(
            name='test3',
            description='test3',
            status=status3,
            executor=self.user,
            author=self.user
        )
        response = self.c.get(
            reverse('tasks_list'),
            content_type='text/html',
            data={'status': status3}
        )
        self.assertNotContains(response, 'test1')
        self.assertTemplateUsed(response, 'tasks.html')

    def test_task_delete_protect(self):
        new_author = MyUser.objects.create_user(
            username='user2',
            password='123'
        )
        protected_task = Task.objects.create(
            name='test4',
            description='test4',
            status=self.status,
            executor=new_author,
            author=new_author
        )
        response = self.c.post(
            reverse('task_delete', kwargs={
                'pk': protected_task.id
            }),
            follow=True
        )
        self.assertAlmostEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(
            protected_task,
            Task.objects.get(id=protected_task.id)
        )

    def test_task_delete(self):
        response = self.c.post(
            reverse('task_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertTemplateUsed(response, 'tasks.html')
        self.assertRaises(Task.DoesNotExist, Task.objects.get, id=1)
