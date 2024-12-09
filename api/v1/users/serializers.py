from rest_framework import serializers

from apps.users.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = User(
            first_name=validated_data["first_name"].strip(),
            last_name=validated_data["last_name"].strip(),
            email=validated_data["email"].strip().lower(),
        )
        user.set_password(validated_data["password"].strip())

        user.is_active = True
        user.save()
        return user
