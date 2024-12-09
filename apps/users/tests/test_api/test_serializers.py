from django.test import TestCase

from api.v1.users.serializers import UserSignupSerializer


class TestUserSignupSerializer(TestCase):
    def setUp(self):
        self.valid_data = {
            "email": "test@example.com",
            "password": "testpass123",  # noqa: S105
            "first_name": "Test",
            "last_name": "User",
        }
        self.serializer = UserSignupSerializer(data=self.valid_data)

    def test_valid_data(self):
        """Test serializer with valid data"""
        self.assertTrue(self.serializer.is_valid())
        user = self.serializer.save()

        self.assertEqual(user.email, self.valid_data["email"].lower())
        self.assertEqual(user.first_name, self.valid_data["first_name"])
        self.assertEqual(user.last_name, self.valid_data["last_name"])
        self.assertTrue(user.check_password(self.valid_data["password"]))

    def test_password_min_length(self):
        """Test password minimum length validation"""
        invalid_data = self.valid_data.copy()
        invalid_data["password"] = "short"  # noqa: S105
        serializer = UserSignupSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_required_fields(self):
        """Test all required fields"""
        required_fields = ["email", "password", "first_name", "last_name"]

        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_data.copy()
                invalid_data.pop(field)
                serializer = UserSignupSerializer(data=invalid_data)

                self.assertFalse(serializer.is_valid())
                self.assertIn(field, serializer.errors)

    def test_email_validation(self):
        """Test email validation"""
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "invalid-email"
        serializer = UserSignupSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
