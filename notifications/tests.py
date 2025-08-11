from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import NotificationTemplate


User = get_user_model()


class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.template = NotificationTemplate.objects.create(
            name='hello', subject='Hi {name}', content='Hello {name}', channel='email'
        )

    def test_send_notification(self):
        url = reverse('notification-send')
        data = {
            'template': self.template.id,
            'users': [self.user.id],
            'context': {'name': 'World'},
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 202)
