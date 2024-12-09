from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ContactInfo,
    EmploymentType,
    Profile,
    Project,
    Review,
    SocialNetwork,
    SpecialistLevel,
    Technology,
)


class SocialNetworkInline(admin.TabularInline):
    model = SocialNetwork
    extra = 1
    fields = ("network_type", "url", "is_primary", "custom_name")


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1
    fields = ("contact_type", "value", "is_primary", "is_public", "label")


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1
    fields = ("title", "status", "start_date", "end_date", "client")
    show_change_link = True


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "profiles_count")
    search_fields = ("name", "code")
    ordering = ("name",)

    def profiles_count(self, obj):
        return obj.profiles.count()

    profiles_count.short_description = "Profiles Count"


@admin.register(SpecialistLevel)
class SpecialistLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "profiles_count")
    search_fields = ("name", "code")
    ordering = ("name",)

    def profiles_count(self, obj):
        return obj.profiles.count()

    profiles_count.short_description = "Profiles Count"


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
        "website_link",
        "profiles_count",
        "projects_count",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "code", "description")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Main Information", {"fields": ("name", "code", "description")}),
        ("Additional Information", {"fields": ("website", "icon", "is_active")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">🔗 Link</a>', obj.website)
        return "-"

    website_link.short_description = "Website"

    def profiles_count(self, obj):
        return obj.profiles.count()

    profiles_count.short_description = "Profiles Count"

    def projects_count(self, obj):
        return obj.projects.count()

    projects_count.short_description = "Projects Count"


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ("profile", "network_type", "custom_name", "is_primary", "url")
    list_filter = ("network_type", "is_primary")
    search_fields = ("profile__first_name", "profile__last_name", "custom_name", "url")
    raw_id_fields = ("profile",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "contact_type",
        "value",
        "is_primary",
        "is_public",
        "is_verified",
    )
    list_filter = ("contact_type", "is_primary", "is_public", "is_verified")
    search_fields = ("profile__first_name", "profile__last_name", "value", "label")
    raw_id_fields = ("profile",)
    readonly_fields = ("verified_at",)

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("profile", "contact_type", "value", "label")},
        ),
        ("Settings", {"fields": ("is_primary", "is_public")}),
        ("Custom Contact", {"fields": ("custom_name",), "classes": ("collapse",)}),
        (
            "Verification",
            {"fields": ("is_verified", "verified_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [ProjectInline, SocialNetworkInline, ContactInfoInline]
    list_display = (
        "thumbnail",  # Добавляем миниатюру в начало списка
        "full_name",
        "position",
        "user_email",
        "level",
        "employment",
        "rating",
    )
    list_filter = ("level", "employment", "technologies")
    search_fields = ("first_name", "last_name", "position", "user__email")
    filter_horizontal = ("technologies",)
    readonly_fields = (
        "rating",
        "review_count",
        "project_count",
        "created_at",
        "updated_at",
        "thumbnail",  # Добавляем в readonly_fields, чтобы показать в detail view
    )
    fieldsets = (
        (
            "User Information",
            {"fields": ("user", "thumbnail", "photo")},
        ),  # Добавляем thumbnail
        ("Basic Information", {"fields": ("first_name", "last_name", "position")}),
        (
            "Professional Information",
            {"fields": ("technologies", "employment", "experience", "level")},
        ),
        (
            "Statistics",
            {
                "fields": ("rating", "review_count", "project_count"),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def thumbnail(self, obj):
        """Return HTML for thumbnail image."""
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.photo,
            )
        return format_html("<span>No photo</span>")

    thumbnail.short_description = "Photo"

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Name"

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User Email"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "level", "employment")
            .prefetch_related("technologies", "projects", "social_networks", "contacts")
        )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "profile",
        "status",
        "start_date",
        "end_date",
        "review_count",
    )
    list_filter = ("status", "technologies")
    search_fields = ("title", "description", "client", "profile__name")
    filter_horizontal = ("technologies",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ["profile"]
    fieldsets = (
        (
            "Project Information",
            {"fields": ("title", "description", "profile", "technologies")},
        ),
        (
            "Project Details",
            {"fields": ("start_date", "end_date", "status", "client", "url", "image")},
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def review_count(self, obj):
        return obj.reviews.count()

    review_count.short_description = "Reviews"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("technologies", "reviews")
            .select_related("profile")
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "reviewer_name",
        "profile",
        "project",
        "rating",
        "is_verified",
        "created_at",
    )
    list_filter = ("is_verified", "rating")
    search_fields = ("reviewer_name", "reviewer_company", "text", "profile__name")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ["profile", "project"]
    fieldsets = (
        ("Review Information", {"fields": ("profile", "project", "rating", "text")}),
        (
            "Reviewer Information",
            {"fields": ("reviewer_name", "reviewer_position", "reviewer_company")},
        ),
        ("Verification", {"fields": ("is_verified", "verified_at")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile", "project")
