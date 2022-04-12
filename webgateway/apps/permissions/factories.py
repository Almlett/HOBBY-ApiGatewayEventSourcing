"""
Factories
"""
import factory
from faker import Factory as FakerFactory
from .models import Permission, Profile, ProfilePermission	# pylint: disable=relative-beyond-top-level

faker = FakerFactory.create()

class PermissionFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for Permission
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model Permission
        """
        model = Permission

    name = "permission_test"
    key = factory.LazyAttribute(lambda x: faker.name())	# pylint: disable=no-member
    description = factory.LazyAttribute(lambda x: faker.text())	# pylint: disable=no-member


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for Profile
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model Profile
        """
        model = Profile

    name = "profile_test"
    key = factory.LazyAttribute(lambda x: faker.name())	# pylint: disable=no-member
    description = factory.LazyAttribute(lambda x: faker.text())	# pylint: disable=no-member

class ProfilePermissionFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for ProfilePermission
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model ProfilePermission
        """
        model = ProfilePermission

    permission = factory.SubFactory(PermissionFactory)	# pylint: disable=no-member
    profile = factory.SubFactory(ProfileFactory)	# pylint: disable=no-member