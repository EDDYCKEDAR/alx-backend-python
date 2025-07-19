from django.test import TestCase
from .models import Message

class MessageModelTest(TestCase):
    def test_create_message(self):
        msg = Message.objects.create(sender="Alice", content="Hello, Bob!")
        self.assertEqual(str(msg), "Alice: Hello, Bob!")
