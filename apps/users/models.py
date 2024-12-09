import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.

        Args:
            email (str): User's email address
            password (str, optional): User's password. Defaults to None.
            **extra_fields: Additional fields to be saved in User model

        Returns:
            User: Created user instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Create and save a superuser with the given email and password.

        Args:
            email (str): Superuser's email address
            password (str, optional): Superuser's password. Defaults to None.

        Returns:
            User: Created superuser instance
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superadmin = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email instead of username for authentication.

    This model extends Django's AbstractBaseUser and PermissionsMixin to create
    a fully featured User model with admin-compliant permissions.
    """

    class Gender(models.TextChoices):
        """Available gender choices for user profile."""

        MALE = "male", "MALE"
        FEMALE = "female", "FEMALE"

    # Unique identifier fields
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user",
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        help_text="User's email address (used for authentication)",
    )

    # Permission fields
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the admin site",
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Designates whether this user account should be considered active",
    )
    is_admin = models.BooleanField(
        default=False,
        help_text="Designates whether the user has admin privileges",
    )

    # Personal information fields
    first_name = models.CharField(
        max_length=255,
        null=True,
        help_text="User's first name",
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        help_text="User's last name",
    )

    # Tracking fields
    last_time_was_online = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of user's last online activity",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        help_text="Timestamp when the user account was created",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        """String representation of the user."""
        return self.email

    def has_perms(self):
        """
        Check if user has any permissions.

        Returns:
            bool: True, as all users have permissions by default
        """
        return True

    def has_module_perms(self, *args, **kwargs):
        """
        Check if user has permission to view the app `app_label`.

        Returns:
            bool: True, as all users have module permissions by default
        """
        return True

    def get_full_name(self):
        """
        Return user's full identifier.

        Returns:
            str: User's email address
        """
        return self.email

    def get_short_name(self):
        """
        Return user's short identifier.

        Returns:
            str: User's email address
        """
        return self.email
