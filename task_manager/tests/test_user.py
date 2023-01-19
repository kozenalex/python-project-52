from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import MyUser


class TestMyUser(TestCase):

    def setUp(self) -> None:
        MyUser.objects.create_user(username='alex_alexov', password='qwerty')
        self.user = MyUser.objects.get(id=1)
        self.c = Client()

    def test_user_login_success(self):
        response = self.c.post(
            reverse('login'),
            data={'username': 'alex_alexov', 'password': 'qwerty'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('index.html')
        self.assertRedirects(response, reverse('index_page'))

    def test_user_create(self):
        response = self.c.post(
            reverse('user_create'),
            data={
                'username': 'foobar',
                'first_name': 'foo',
                'last_name': 'bar',
                'email': 'foo@bar.mp3',
                'password': 'asdfgh'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

    def test_user_update(self):
        self.c.post(
            reverse('login'),
            data={'username': 'alex_alexov', 'password': 'qwerty'},
            follow=True
        )
        response = self.c.post(
            reverse('user_update', kwargs={'pk': 1}),
            data={
                'username': 'foobar',
                'first_name': 'foo',
                'last_name': 'bar',
                'email': 'foo@bar.mp3',
                'password': 'asdfgh'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users_list'))
        self.assertTemplateUsed(response, 'users.html')

    def test_user_delete(self):
        self.c.post(
            reverse('login'),
            data={'username': 'alex_alexov', 'password': 'qwerty'},
            follow=True
        )
        MyUser.objects.create_user(username='del_udal', password='qwerty')
        response = self.c.post(
            reverse('user_delete', kwargs={'pk': 2}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users_list'))
        self.assertTemplateUsed(response, 'users.html')
