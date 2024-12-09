import pytest
from django.test import TestCase

from apps.users.models import User


class TestUserManager(TestCase):
    def setUp(self):
        self.test_password = "test_pass_123"  # noqa: S105
        self.test_email = "test@example.com"
        self.admin_email = "admin@example.com"

    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email=self.test_email,
            password=self.test_password,
        )

        self.assertEqual(user.email, self.test_email)
        self.assertTrue(user.check_password(self.test_password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_active)

    def test_create_user_without_email(self):
        """Test creating a user without email raises error"""
        with pytest.raises(ValueError, match="Users must have an email address"):
            User.objects.create_user(email="", password=self.test_password)

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            email=self.admin_email,
            password=self.test_password,
        )

        self.assertEqual(user.email, self.admin_email)
        self.assertTrue(user.check_password(self.test_password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superadmin)
