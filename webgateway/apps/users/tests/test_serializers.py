"""
test for app users
"""
import json
import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from users.models import ApiUser,UserProfile, UserPermission	# pylint: disable=relative-beyond-top-level
from users.serializers import ApiUserSerializer, UserProfileSerializer, UserPermissionSerializer	# pylint: disable=relative-beyond-top-level

from users.models import Turn, Department, UserDepartment	# pylint: disable=relative-beyond-top-level
from users.serializers import TurnSerializer, DepartmentSerializer, UserDepartmentSerializer	# pylint: disable=relative-beyond-top-level


from permissions.models import Profile, Permission
from permissions.serializers import ProfileSerializer, PermissionSerializer

pytestmark = pytest.mark.django_db


class TestApiUserSerializer:
    """
    Test for ApiUserSerializer
    """

    def test_expected_serialized_json(self,api_user_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        apiuser_created = api_user_factory()
        apiuser = ApiUser.objects.get(id = apiuser_created.id)
        results = ApiUserSerializer(apiuser).data

        assert results['username'] == "user_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
            'email':'email@test.com'
        }

        serializer = ApiUserSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestUserProfileSerializer:
    """
    Test for UserProfileSerializer
    """

    def test_expected_serialized_json(self,user_profile_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        user_profile_created = user_profile_factory()
        user_profile = UserProfile.objects.get(id = user_profile_created.id)
        results = UserProfileSerializer(user_profile).data
        profile = Profile.objects.get(id = results['profile'])
        assert str(profile) == "profile_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = UserProfileSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestUserPermissionSerializer:
    """
    Test for UserPermissionSerializer
    """

    def test_expected_serialized_json(self,user_permission_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        user_permission_created = user_permission_factory()
        user_permission = UserPermission.objects.get(id = user_permission_created.id)
        results = UserPermissionSerializer(user_permission).data
        permission = Permission.objects.get(id = results['permission'])
        assert str(permission) == "permission_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = UserPermissionSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestTurnSerializer:
    """
    Test for TurnSerializer
    """

    def test_expected_serialized_json(self,turn_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        turn_created = turn_factory()
        turn = Turn.objects.get(id = turn_created.id)
        results = TurnSerializer(turn).data
        assert str(turn) == "turn_test"
        assert results['name'] == "turn_test", 'Name should be turn_test'
        assert str(results['start_time']) == "07:00:00", 'Start time should be 07:00:00'
        assert str(results['end_time']) == "12:00:00", 'End time should be 12:00:00'

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
            'name':'test'
        }

        serializer = TurnSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestDepartmentSerializer:
    """
    Test for DepartmentSerializer
    """

    def test_expected_serialized_json(self,department_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        department_created = department_factory()
        department = Department.objects.get(id = department_created.id)
        results = DepartmentSerializer(department).data
        assert str(department) == "department_test"
        assert str(results['name']) == "department_test", 'Name should be department_test'
        
    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = DepartmentSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestUserDepartmentSerializer:
    """
    Test for UserDepartmentSerializer
    """

    def test_expected_serialized_json(self,user_department_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        user_department_created = user_department_factory()
        user_department = UserDepartment.objects.get(id = user_department_created.id)
        results = UserDepartmentSerializer(user_department).data
        user = ApiUser.objects.get(id = results['user'])
        department = Department.objects.get(id = results['department'])
        turn = Turn.objects.get(id = results['turn'])
        manager = results['manager']

        assert str(user) == "user_test"
        assert str(department) == "department_test"
        assert str(turn) == "turn_test"
        assert manager == True

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = UserDepartmentSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)