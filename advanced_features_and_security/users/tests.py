from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class CustomUserTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            date_of_birth='1990-01-01'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.date_of_birth, '1990-01-01')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_str_method(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'testuser')

    def test_user_without_username(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                username='',
                email='test@example.com',
                password='testpass123'
            )

    def test_user_without_email(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                username='testuser',
                email='',
                password='testpass123'
            )
