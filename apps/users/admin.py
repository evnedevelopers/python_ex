from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


class UserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for the User model.
    Extends Django's built-in UserAdmin to customize the admin interface
    for our custom User model.
    """

    # Number of items to display per page in the admin list view
    list_per_page = 100

    # Fields to display in the admin list view
    list_display = (
        "uuid",
        "first_name",
        "last_name",
        "email",
        "created_at",
    )

    # Configuration for editing existing users
    fieldsets = (
        (
            None,  # Section header (None means no header)
            {
                "fields": (
                    "uuid",
                    "email",
                    "password",
                    "last_time_was_online",
                ),
            },
        ),
    )

    # Configuration for adding new users
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),  # CSS classes for the form section
                "fields": (
                    "email",
                    "password1",
                    "password2",  # Password confirmation field
                ),
            },
        ),
    )

    # Fields that cannot be modified through the admin interface
    readonly_fields = (
        "uuid",
        "created_at",
    )

    # Fields that can be used to search for users in the admin interface
    search_fields = (
        "uuid",
        "email",
        "created_at",
    )

    # Default ordering for the list view
    ordering = ("-created_at",)

    # Many-to-many fields that should use horizontal selection widget
    # Empty tuple as we don't have any many-to-many fields currently
    filter_horizontal = ()


# Register the User model with its custom admin configuration
admin.site.register(User, UserAdmin)
