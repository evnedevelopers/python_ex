from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.profiles.models import EmploymentType, Profile, SpecialistLevel, Technology

from .serializers import ProfileDetailSerializer, ProfileListSerializer


class ProfileFilter(filters.FilterSet):
    technology = filters.ModelMultipleChoiceFilter(
        field_name="technologies__code",
        to_field_name="code",
        queryset=Technology.objects.all(),
    )
    employment = filters.ModelChoiceFilter(
        field_name="employment__code",
        to_field_name="code",
        queryset=EmploymentType.objects.all(),
    )
    level = filters.ModelChoiceFilter(
        field_name="level__code",
        to_field_name="code",
        queryset=SpecialistLevel.objects.all(),
    )
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    min_experience = filters.NumberFilter(field_name="experience", lookup_expr="gte")

    class Meta:
        model = Profile
        fields = ["technology", "employment", "level", "min_rating", "min_experience"]


class ProfileListView(generics.ListCreateAPIView):
    """
    List and create profiles
    """

    queryset = Profile.objects.select_related("employment", "level").prefetch_related(
        "technologies",
    )
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProfileFilter
    ordering_fields = ["rating", "review_count", "project_count", "created_at"]
    search_fields = ["first_name", "last_name", "position"]


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a profile
    """

    queryset = Profile.objects.select_related("employment", "level").prefetch_related(
        "technologies",
        "social_networks",
        "contacts",
        "projects",
        "projects__technologies",
        "projects__reviews",
        "reviews",
    )
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]
