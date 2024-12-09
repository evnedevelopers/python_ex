from rest_framework import serializers

from apps.profiles.models import (
    ContactInfo,
    EmploymentType,
    Profile,
    Project,
    Review,
    SocialNetwork,
    SpecialistLevel,
    Technology,
)


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "code", "description", "website", "icon"]


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ["id", "name", "code"]


class SpecialistLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistLevel
        fields = ["id", "name", "code"]


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ["id", "network_type", "url", "is_primary", "custom_name"]


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            "id",
            "contact_type",
            "value",
            "is_primary",
            "is_public",
            "custom_name",
            "label",
            "is_verified",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "rating",
            "text",
            "reviewer_name",
            "reviewer_position",
            "reviewer_company",
            "is_verified",
            "created_at",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "technologies",
            "start_date",
            "end_date",
            "status",
            "client",
            "url",
            "image",
            "reviews",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)
    employment = EmploymentTypeSerializer()
    level = SpecialistLevelSerializer()
    social_networks = SocialNetworkSerializer(many=True)
    contacts = ContactInfoSerializer(many=True)
    projects = ProjectSerializer(many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "photo",
            "first_name",
            "last_name",
            "position",
            "technologies",
            "employment",
            "experience",
            "level",
            "rating",
            "review_count",
            "project_count",
            "social_networks",
            "contacts",
            "projects",
            "reviews",
            "created_at",
            "updated_at",
        ]
