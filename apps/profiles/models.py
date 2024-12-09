from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.users.models import User


class EmploymentType(models.Model):
    """Model representing different types of employment for specialists.

    This model stores various employment types such as full-time, part-time,
    contract, etc.
    """

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        """Return string representation of the employment type."""
        return self.name

    class Meta:
        """Meta options for EmploymentType model."""

        ordering = ["name"]


class SpecialistLevel(models.Model):
    """Model representing different levels of specialists.

    This model stores various specialist levels such as junior, middle,
    senior, etc.
    """

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        """Return string representation of the specialist level."""
        return self.name

    class Meta:
        """Meta options for SpecialistLevel model."""

        ordering = ["name"]


class Technology(models.Model):
    """Model representing technologies used by specialists.

    This model stores various technologies, frameworks, and tools used
    in projects and by specialists.
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    # Optional fields
    website = models.URLField(blank=True)
    icon = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the technology."""
        return self.name

    class Meta:
        """Meta options for Technology model."""

        verbose_name_plural = "Technologies"
        ordering = ["name"]


class Profile(models.Model):
    """Model representing a specialist's profile.

    This model stores comprehensive information about a specialist including
    their personal details, professional information, and statistics.
    """

    # Basic Information
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profiles",
    )
    photo = models.URLField(blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    # Professional Information
    technologies = models.ManyToManyField(Technology, related_name="profiles")
    employment = models.ForeignKey(
        EmploymentType,
        on_delete=models.PROTECT,
        related_name="profiles",
    )
    experience = models.CharField(max_length=20)
    level = models.ForeignKey(
        SpecialistLevel,
        on_delete=models.PROTECT,
        related_name="profiles",
    )
    # Statistics
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    review_count = models.PositiveIntegerField(default=0)
    project_count = models.PositiveIntegerField(default=0)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the profile."""
        return f"{self.first_name} {self.last_name} - {self.position}"

    class Meta:
        """Meta options for Profile model."""

        ordering = ["-rating", "-review_count"]


class SocialNetwork(models.Model):
    """Model representing social network links for profiles.

    This model stores various social media profiles associated with a specialist's
    profile.
    """

    NETWORK_TYPES = [
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("gitlab", "GitLab"),
        ("twitter", "Twitter"),
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("medium", "Medium"),
        ("dev_to", "Dev.to"),
        ("stackoverflow", "Stack Overflow"),
        ("behance", "Behance"),
        ("dribbble", "Dribbble"),
        ("other", "Other"),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="social_networks",
    )
    network_type = models.CharField(max_length=20, choices=NETWORK_TYPES)
    url = models.URLField()
    is_primary = models.BooleanField(default=False)
    # For custom networks
    custom_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        """Return string representation of the social network link."""
        if self.network_type == "other":
            return f"{self.custom_name} - {self.profile.first_name}"
        return f"{self.network_type} - {self.profile.first_name}"

    class Meta:
        """Meta options for SocialNetwork model."""

        ordering = ["-is_primary", "network_type"]
        unique_together = ["profile", "network_type"]


class ContactInfo(models.Model):
    """Model representing contact information for profiles.

    This model stores various contact methods and details associated with
    a specialist's profile.
    """

    CONTACT_TYPES = [
        ("phone", "Phone"),
        ("email", "Email"),
        ("telegram", "Telegram"),
        ("whatsapp", "WhatsApp"),
        ("viber", "Viber"),
        ("skype", "Skype"),
        ("discord", "Discord"),
        ("slack", "Slack"),
        ("wechat", "WeChat"),
        ("signal", "Signal"),
        ("other", "Other"),
    ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    value = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    # For custom contact types
    custom_name = models.CharField(max_length=50, blank=True)
    # Additional fields
    label = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., 'Work Phone', 'Personal Email'",
    )
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return string representation of the contact information."""
        if self.label:
            return f"{self.label}: {self.value}"
        return f"{self.contact_type}: {self.value}"

    class Meta:
        """Meta options for ContactInfo model."""

        ordering = ["-is_primary", "contact_type"]
        unique_together = ["profile", "contact_type", "value"]


class Project(models.Model):
    """Model representing projects associated with profiles.

    This model stores information about projects that specialists have worked on
    or are currently working on.
    """

    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.ManyToManyField(Technology, related_name="projects")
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    # Project details
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ongoing")
    # Optional fields
    client = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    image = models.URLField(blank=True)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the project."""
        return f"{self.title} - {self.profile.first_name} {self.profile.last_name}"

    class Meta:
        """Meta options for Project model."""

        ordering = ["-start_date"]


class Review(models.Model):
    """Model representing reviews for profiles.

    This model stores reviews and ratings given to specialists, optionally
    associated with specific projects.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    # Review details
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField()
    reviewer_name = models.CharField(max_length=100)
    reviewer_position = models.CharField(max_length=100, blank=True)
    reviewer_company = models.CharField(max_length=100, blank=True)
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the review."""
        return f"Review for {self.profile.name} by {self.reviewer_name}"

    class Meta:
        """Meta options for Review model."""

        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Override save method to update profile statistics."""
        if not self.pk:
            self.profile.review_count += 1
            all_ratings = list(self.profile.reviews.values_list("rating", flat=True))
            all_ratings.append(self.rating)
            self.profile.rating = sum(all_ratings) / len(all_ratings)
            self.profile.save()
        super().save(*args, **kwargs)
