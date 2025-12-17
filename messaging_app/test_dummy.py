# messaging_app/listings/tests/test_dummy.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class DummyTest(TestCase):
    def test_dummy_addition(self):
        """A simple dummy test"""
        self.assertEqual(1 + 1, 2)

    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create_user(username="testuser", password="pass123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("pass123"))
