import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

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
from apps.users.tests.factories import UserFactory


class EmploymentTypeFactory(DjangoModelFactory):
    class Meta:
        model = EmploymentType

    name = factory.Sequence(lambda n: f"Employment Type {n}")
    code = factory.Sequence(lambda n: f"type_{n}")


class SpecialistLevelFactory(DjangoModelFactory):
    class Meta:
        model = SpecialistLevel

    name = factory.Sequence(lambda n: f"Level {n}")
    code = factory.Sequence(lambda n: f"level_{n}")


class TechnologyFactory(DjangoModelFactory):
    class Meta:
        model = Technology

    name = factory.Sequence(lambda n: f"Technology {n}")
    code = factory.Sequence(lambda n: f"tech_{n}")
    description = factory.Faker("text")
    website = factory.Faker("url")
    is_active = True
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    photo = factory.Faker("url")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    position = factory.Faker("job")
    employment = factory.SubFactory(EmploymentTypeFactory)
    experience = factory.Sequence(lambda n: f"{n}+ years")
    level = factory.SubFactory(SpecialistLevelFactory)
    rating = factory.Faker(
        "pydecimal",
        left_digits=1,
        right_digits=1,
        positive=True,
        max_value=5,
    )
    review_count = 0
    project_count = 0

    @factory.post_generation
    def technologies(self, create, extracted):
        if not create:
            return

        if extracted:
            for technology in extracted:
                self.technologies.add(technology)


class SocialNetworkFactory(DjangoModelFactory):
    class Meta:
        model = SocialNetwork

    profile = factory.SubFactory(ProfileFactory)
    network_type = factory.Iterator(
        ["linkedin", "github", "gitlab", "twitter", "facebook", "instagram", "youtube"],
    )
    url = factory.Faker("url")
    is_primary = False


class ContactInfoFactory(DjangoModelFactory):
    class Meta:
        model = ContactInfo

    profile = factory.SubFactory(ProfileFactory)
    contact_type = factory.Iterator(
        ["phone", "email", "telegram", "whatsapp", "viber", "skype", "discord"],
    )
    value = factory.Faker("email")
    is_primary = False
    is_public = True


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Faker("catch_phrase")
    description = factory.Faker("text")
    profile = factory.SubFactory(ProfileFactory)
    start_date = factory.Faker("date_object")
    status = "ongoing"
    client = factory.Faker("company")
    url = factory.Faker("url")
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def technologies(self, create, extracted):
        if not create:
            return

        if extracted:
            for technology in extracted:
                self.technologies.add(technology)


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    profile = factory.SubFactory(ProfileFactory)
    project = factory.SubFactory(ProjectFactory)
    rating = factory.Iterator([1, 2, 3, 4, 5])
    text = factory.Faker("text")
    reviewer_name = factory.Faker("name")
    reviewer_position = factory.Faker("job")
    reviewer_company = factory.Faker("company")
    is_verified = False
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
