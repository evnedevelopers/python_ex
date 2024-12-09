from rest_framework import serializers

from apps.profiles.models import EmploymentType, SpecialistLevel, Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "code"]


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ["id", "name", "code"]


class SpecialistLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistLevel
        fields = ["id", "name", "code"]
