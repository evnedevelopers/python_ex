from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

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

from .factories import (
    ContactInfoFactory,
    EmploymentTypeFactory,
    ProfileFactory,
    ProjectFactory,
    ReviewFactory,
    SocialNetworkFactory,
    SpecialistLevelFactory,
    TechnologyFactory,
)

# Constants for tests
TECHNOLOGIES_COUNT = 3
REVIEW_COUNT = 2
MIN_RATING = 1
MAX_RATING = 5
INVALID_HIGH_RATING = 6
INVALID_LOW_RATING = 0
ZERO_DECIMAL = Decimal("0.0")
MAX_RATING_DECIMAL = Decimal("5.0")
ABOVE_MAX_RATING = Decimal("5.1")
BELOW_MIN_RATING = Decimal("-0.1")
AVERAGE_RATING_DECIMAL = Decimal("3.0")


@pytest.mark.django_db
class TestEmploymentType:
    def test_create_employment_type(self):
        employment = EmploymentTypeFactory()
        assert isinstance(employment, EmploymentType)
        assert employment.name
        assert employment.code

    def test_unique_constraints(self):
        employment = EmploymentTypeFactory()

        with pytest.raises(IntegrityError), transaction.atomic():
            EmploymentTypeFactory(name=employment.name)

        with pytest.raises(IntegrityError), transaction.atomic():
            EmploymentTypeFactory(code=employment.code)

    def test_str_representation(self):
        employment = EmploymentTypeFactory(name="Full-time")
        assert str(employment) == "Full-time"


@pytest.mark.django_db
class TestSpecialistLevel:
    def test_create_specialist_level(self):
        level = SpecialistLevelFactory()
        assert isinstance(level, SpecialistLevel)
        assert level.name
        assert level.code

    def test_unique_constraints(self):
        level = SpecialistLevelFactory()

        with pytest.raises(IntegrityError), transaction.atomic():
            SpecialistLevelFactory(name=level.name)

        with pytest.raises(IntegrityError), transaction.atomic():
            SpecialistLevelFactory(code=level.code)


@pytest.mark.django_db
class TestTechnology:
    def test_create_technology(self):
        tech = TechnologyFactory()
        assert isinstance(tech, Technology)
        assert tech.name
        assert tech.code
        assert tech.created_at
        assert tech.updated_at

    def test_unique_constraints(self):
        tech = TechnologyFactory()

        with pytest.raises(IntegrityError), transaction.atomic():
            TechnologyFactory(name=tech.name)

        with pytest.raises(IntegrityError), transaction.atomic():
            TechnologyFactory(code=tech.code)

    def test_optional_fields(self):
        tech = TechnologyFactory(website="", icon="", description="")
        assert tech.website == ""
        assert tech.icon == ""
        assert tech.description == ""


@pytest.mark.django_db
class TestProfile:
    def test_create_profile(self):
        profile = ProfileFactory()
        assert isinstance(profile, Profile)
        assert profile.first_name
        assert profile.last_name
        assert profile.position

    def test_profile_with_technologies(self):
        technologies = TechnologyFactory.create_batch(TECHNOLOGIES_COUNT)
        profile = ProfileFactory()
        profile.technologies.set(technologies)
        assert profile.technologies.count() == TECHNOLOGIES_COUNT

    def test_high_rating_validation(self):
        profile = ProfileFactory(rating=ABOVE_MAX_RATING)
        with pytest.raises(ValidationError):
            profile.full_clean()

    def test_negative_rating_validation(self):
        profile = ProfileFactory(rating=BELOW_MIN_RATING)
        with pytest.raises(ValidationError):
            profile.full_clean()


@pytest.mark.django_db
class TestSocialNetwork:
    def test_create_social_network(self):
        social = SocialNetworkFactory()
        assert isinstance(social, SocialNetwork)
        assert social.profile
        assert social.network_type
        assert social.url

    def test_unique_network_type_per_profile(self):
        social = SocialNetworkFactory(network_type="github")

        with pytest.raises(IntegrityError), transaction.atomic():
            SocialNetworkFactory(profile=social.profile, network_type="github")

    def test_custom_network_type(self):
        social = SocialNetworkFactory(
            network_type="other",
            custom_name="Custom Network",
        )
        assert social.custom_name == "Custom Network"


@pytest.mark.django_db
class TestContactInfo:
    def test_create_contact_info(self):
        contact = ContactInfoFactory()
        assert isinstance(contact, ContactInfo)
        assert contact.profile
        assert contact.contact_type
        assert contact.value

    def test_unique_contact_per_profile(self):
        contact = ContactInfoFactory(contact_type="email", value="test@example.com")

        with pytest.raises(IntegrityError), transaction.atomic():
            ContactInfoFactory(
                profile=contact.profile,
                contact_type="email",
                value="test@example.com",
            )


@pytest.mark.django_db
class TestProject:
    def test_create_project(self):
        project = ProjectFactory()
        assert isinstance(project, Project)
        assert project.title
        assert project.description
        assert project.start_date

    def test_project_with_technologies(self):
        technologies = TechnologyFactory.create_batch(TECHNOLOGIES_COUNT)
        project = ProjectFactory()
        project.technologies.set(technologies)
        assert project.technologies.count() == TECHNOLOGIES_COUNT

    def test_project_status(self):
        project = ProjectFactory(status="completed")
        assert project.status == "completed"


@pytest.mark.django_db
class TestReview:
    def test_create_review(self):
        review = ReviewFactory()
        assert isinstance(review, Review)
        assert review.profile
        assert MIN_RATING <= review.rating <= MAX_RATING
        assert review.text

    def test_review_updates_profile_stats(self):
        profile = ProfileFactory(rating=ZERO_DECIMAL, review_count=0)
        ReviewFactory(profile=profile, rating=MAX_RATING)
        profile.refresh_from_db()
        assert profile.review_count == 1
        assert profile.rating == MAX_RATING_DECIMAL

    def test_multiple_reviews_calculation(self):
        profile = ProfileFactory(rating=ZERO_DECIMAL, review_count=0)
        ReviewFactory(profile=profile, rating=MAX_RATING)
        ReviewFactory(profile=profile, rating=MIN_RATING)

        profile.refresh_from_db()
        assert profile.review_count == REVIEW_COUNT
        assert profile.rating == AVERAGE_RATING_DECIMAL

    def test_high_rating_validation(self):
        with pytest.raises(ValidationError):
            ReviewFactory(rating=INVALID_HIGH_RATING).full_clean()

    def test_zero_rating_validation(self):
        with pytest.raises(ValidationError):
            ReviewFactory(rating=INVALID_LOW_RATING).full_clean()
