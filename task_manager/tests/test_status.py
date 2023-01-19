from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import MyUser, Status


class TestStatus(TestCase):

    def setUp(self) -> None:
        MyUser.objects.create_user(username='alex_alexov', password='qwerty')
        Status.objects.create(name='test')
        self.c = Client()
        self.c.post(
            reverse('login'),
            data={'username': 'alex_alexov', 'password': 'qwerty'}
        )

    def test_status_create(self):
        response = self.c.post(
            reverse('status_create'),
            data={
                'name': 'test1'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTemplateUsed(response, 'statuses.html')

    def test_status_update(self):
        response = self.c.post(
            reverse('status_update', kwargs={'pk': 1}),
            data={'name': 'test2'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTemplateUsed(response, 'statuses.html')

    def test_status_delete(self):
        response = self.c.post(
            reverse('status_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('statuses_list'))
        self.assertTemplateUsed(response, 'statuses.html')
