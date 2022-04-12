"""
test for app users
"""
import json
import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from permissions.models import Permission, Profile, ProfilePermission	# pylint: disable=relative-beyond-top-level
from permissions.serializers import PermissionSerializer, ProfileSerializer, ProfilePermissionSerializer	# pylint: disable=relative-beyond-top-level

pytestmark = pytest.mark.django_db


class TestPermissionSerializer:
    """
    Test for PermissionSerializer
    """

    def test_expected_serialized_json(self,permission_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        permission_created = permission_factory()
        permission = Permission.objects.get(id = permission_created.id)
        results = PermissionSerializer(permission).data

        assert results['name'] == "permission_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = PermissionSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

class TestProfileSerializer:
    """
    Test for ProfileSerializer
    """

    def test_expected_serialized_json(self,profile_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        profile_created = profile_factory()
        profile = Profile.objects.get(id = profile_created.id)
        results = ProfileSerializer(profile).data

        assert results['name'] == "profile_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = ProfileSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

class TestProfilePermissionSerializer:
    """
    Test for ProfilePermissionSerializer
    """

    def test_expected_serialized_json(self,profile_permission_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        profile_permission_created = profile_permission_factory()
        profile_permission = ProfilePermission.objects.get(id = profile_permission_created.id)
        results = ProfilePermissionSerializer(profile_permission).data
        profile = Profile.objects.get(id = results['profile'])
        assert str(profile) == "profile_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = ProfilePermissionSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
