from django.test import TestCase, Client
from django.urls import reverse
from task.models import Task
from users.models import MyUser
from labels.models import Labels
from statuses.models import Status


class TestLabels(TestCase):

    def setUp(self) -> None:
        MyUser.objects.create_user(username='alex_alexov', password='qwerty')
        Labels.objects.create(name='test')
        self.c = Client()
        self.c.post(
            reverse('login'),
            data={'username': 'alex_alexov', 'password': 'qwerty'}
        )
        self.user = MyUser.objects.get(id=1)
        self.label = Labels.objects.get(id=1)
        self.status = Status.objects.create(name='teststatus')

    def test_label_create(self):
        response = self.c.post(
            reverse('label_create'),
            data={
                'name': 'test1'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTemplateUsed(response, 'labels.html')

    def test_label_update(self):
        response = self.c.post(
            reverse('label_update', kwargs={'pk': 1}),
            data={'name': 'test2'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTemplateUsed(response, 'labels.html')

    def test_labels_list(self):
        Labels.objects.create(name='test3')
        response = self.c.get(
            reverse('labels_list')
        )
        self.assertTemplateUsed(response, 'labels.html')
        self.assertEqual(response.status_code, 200)
        for label in Labels.objects.all():
            self.assertContains(response, label.name)

    def test_label_delete_protect(self):
        task = Task.objects.create(
            name='test',
            author=self.user,
            executor=self.user,
            status=self.status
        )
        task.labels.add(self.label)
        response = self.c.post(
            reverse('label_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTemplateUsed(response, 'labels.html')

    def test_label_delete(self):
        response = self.c.post(
            reverse('label_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('labels_list'))
        self.assertTemplateUsed(response, 'labels.html')
