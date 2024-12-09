from rest_framework import serializers

from apps.profiles.models import ContactInfo, SocialNetwork


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ["id", "network_type", "url", "is_primary"]


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            "id",
            "contact_type",
            "value",
            "is_primary",
            "is_public",
            "label",
            "is_verified",
        ]
