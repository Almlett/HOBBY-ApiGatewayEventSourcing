"""
test for app users
"""
import json
import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from permissions.models import Permission, Profile, ProfilePermission	# pylint: disable=relative-beyond-top-level

pytestmark = pytest.mark.django_db

class TestPermission:
    """
    Test Permission Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, permission_factory,):	# pylint: disable=no-self-use
        """
        test created permission
        """

        permission_created = permission_factory()
        permission = Permission.objects.get(id = permission_created.id)
        assert permission.name == "permission_test", 'Name should be permission_test'
        assert str(permission) == "permission_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, permission_factory,):	# pylint: disable=no-self-use
        """
        test updated permission
        """

        permission_created = permission_factory()
        permission = Permission.objects.get(id = permission_created.id)

        permission.name = "permission_test2"
        permission.save()
        assert permission.name == "permission_test2", 'name should be permission_test2'

class TestProfile:
    """
    Test Profile Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, profile_factory,):	# pylint: disable=no-self-use
        """
        test created profile
        """

        profile_created = profile_factory()
        profile = Profile.objects.get(id = profile_created.id)
        assert profile.name == "profile_test", 'Name should be profile_test'
        assert str(profile) == "profile_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, profile_factory,):	# pylint: disable=no-self-use
        """
        test updated profile
        """

        profile_created = profile_factory()
        profile = Profile.objects.get(id = profile_created.id)

        profile.name = "profile_test2"
        profile.save()
        assert profile.name == "profile_test2", 'name should be profile_test2'


class TestProfilePermission:
    """
    Test ProfilePermission Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, profile_permission_factory,):	# pylint: disable=no-self-use
        """
        test created profile_permission
        """

        profile_permission_created = profile_permission_factory()
        profile_permission = ProfilePermission.objects.get(id = profile_permission_created.id)
        assert profile_permission.profile.name == "profile_test", 'Name should be profile_permission_test'
        assert str(profile_permission) == "profile_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, profile_permission_factory,):	# pylint: disable=no-self-use
        """
        test updated profile_permission
        """
        profile_test = Profile()
        profile_test.name="profile_permission_test2"
        profile_test.key="test"
        profile_test.description="test"
        profile_test.save()


        profile_permission_created = profile_permission_factory()
        profile_permission = ProfilePermission.objects.get(id = profile_permission_created.id)

        profile_permission.profile = profile_test
        profile_permission.save()

        assert profile_permission.profile.name == "profile_permission_test2", 'name should be profile_permission_test2'

