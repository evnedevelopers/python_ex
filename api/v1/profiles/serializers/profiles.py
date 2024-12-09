from rest_framework import serializers

from apps.profiles.models import Profile

from .base import (
    EmploymentTypeSerializer,
    SpecialistLevelSerializer,
    TechnologySerializer,
)
from .contacts import ContactInfoSerializer, SocialNetworkSerializer
from .projects import ProjectDetailSerializer
from .reviews import ReviewDetailSerializer


class ProfileListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка профилей с основной информацией."""

    technologies = TechnologySerializer(many=True)
    employment = EmploymentTypeSerializer()
    level = SpecialistLevelSerializer()

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
            "level",
            "experience",
            "rating",
            "review_count",
            "project_count",
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о профиле."""

    technologies = TechnologySerializer(many=True)
    employment = EmploymentTypeSerializer()
    level = SpecialistLevelSerializer()
    social_networks = SocialNetworkSerializer(many=True)
    contacts = ContactInfoSerializer(many=True)
    projects = ProjectDetailSerializer(many=True)
    reviews = ReviewDetailSerializer(many=True)

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
