from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class TestJWTAuthenticationView(APITestCase):
    def setUp(self):
        self.token_obtain_url = reverse("api:auth:token_obtain_pair")
        self.token_refresh_url = reverse("api:auth:token_refresh")
        self.token_verify_url = reverse("api:auth:token_verify")

        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,  # Важно, так как по умолчанию is_active=False
        }
        self.user = User.objects.create_user(**self.user_data)

        # Данные для логина через email
        self.login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }

    def test_obtain_token_pair_success(self):
        """Test successful token pair obtaining"""
        response = self.client.post(
            self.token_obtain_url,
            self.login_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_pair_invalid_credentials(self):
        """Test token pair obtaining with invalid credentials"""
        invalid_data = {
            "email": self.login_data["email"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.token_obtain_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        # First obtain tokens
        response = self.client.post(
            self.token_obtain_url,
            self.login_data,
            format="json",
        )
        refresh_token = response.data["refresh"]

        # Then try to refresh
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(self.token_refresh_url, refresh_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_invalid(self):
        """Test token refresh with invalid refresh token"""
        invalid_data = {"refresh": "invalid-refresh-token"}
        response = self.client.post(self.token_refresh_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_token_success(self):
        """Test successful token verification"""
        # First obtain tokens
        response = self.client.post(
            self.token_obtain_url,
            self.login_data,
            format="json",
        )
        access_token = response.data["access"]

        # Then verify the access token
        verify_data = {"token": access_token}
        response = self.client.post(self.token_verify_url, verify_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_invalid(self):
        """Test token verification with invalid token"""
        invalid_data = {"token": "invalid-token"}
        response = self.client.post(self.token_verify_url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_missing_fields(self):
        """Test token obtaining with missing required fields"""
        required_fields = ["email", "password"]
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.login_data.copy()
                invalid_data.pop(field)
                response = self.client.post(
                    self.token_obtain_url,
                    invalid_data,
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_inactive_user(self):
        """Test token obtaining with inactive user"""
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.token_obtain_url,
            self.login_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestSignupView(APITestCase):
    def setUp(self):
        self.signup_url = reverse("api:users:signup")
        self.valid_payload = {
            "email": "test@example.com",
            "password": "testpass123",  # noqa: S105
            "first_name": "Test",
            "last_name": "User",
        }

    def test_successful_signup(self):
        """Test successful user registration"""
        response = self.client.post(self.signup_url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.valid_payload["email"].lower())

    def test_invalid_email(self):
        """Test signup with invalid email"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "invalid-email"

        response = self.client.post(self.signup_url, invalid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_missing_required_fields(self):
        """Test signup with missing required fields"""
        required_fields = ["email", "password", "first_name", "last_name"]

        for field in required_fields:
            with self.subTest(field=field):
                invalid_payload = self.valid_payload.copy()
                invalid_payload.pop(field)

                response = self.client.post(
                    self.signup_url,
                    invalid_payload,
                    format="json",
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(User.objects.count(), 0)

    def test_duplicate_email(self):
        """Test signup with already registered email"""
        # First registration
        self.client.post(self.signup_url, self.valid_payload, format="json")

        # Try to register with same email
        response = self.client.post(self.signup_url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
