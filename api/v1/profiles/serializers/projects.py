from rest_framework import serializers

from apps.profiles.models import Project

from .base import TechnologySerializer
from .reviews import ReviewDetailSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Project
        fields = ["id", "title", "technologies", "start_date", "end_date", "status"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)
    reviews = ReviewDetailSerializer(many=True, read_only=True)

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
            "created_at",
            "updated_at",
        ]
