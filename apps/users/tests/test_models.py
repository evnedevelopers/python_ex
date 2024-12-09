import pytest
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.users.models import User


class TestUser(TestCase):
    def setUp(self):
        self.test_password = "test_pass_123"  # noqa: S105
        self.user_data = {
            "email": "test@example.com",
            "password": self.test_password,
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )

    def test_user_creation(self):
        """Test user creation with all fields"""
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertIsNotNone(self.user.uuid)
        self.assertIsNotNone(self.user.created_at)

    def test_str_representation(self):
        """Test string representation of user"""
        self.assertEqual(str(self.user), self.user_data["email"])

    def test_get_full_name(self):
        """Test get_full_name method"""
        self.assertEqual(self.user.get_full_name(), self.user_data["email"])

    def test_get_short_name(self):
        """Test get_short_name method"""
        self.assertEqual(self.user.get_short_name(), self.user_data["email"])

    def test_create_user_without_email(self):
        """Test creating a user without email raises error"""
        with pytest.raises(ValueError, match="Users must have an email address"):
            User.objects.create_user(email="", password=self.test_password)

    def test_email_uniqueness(self):
        """Test that duplicate emails are not allowed"""
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email=self.user_data["email"],
                password=self.test_password,
            )
