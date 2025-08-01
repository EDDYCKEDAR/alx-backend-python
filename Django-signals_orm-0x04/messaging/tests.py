# === messaging/tests.py ===
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')

    def test_message_creates_notification(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        self.assertEqual(Notification.objects.count(), 1)
