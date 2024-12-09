from rest_framework import serializers

from apps.profiles.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "reviewer_name", "created_at"]


class ReviewDetailSerializer(serializers.ModelSerializer):
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
