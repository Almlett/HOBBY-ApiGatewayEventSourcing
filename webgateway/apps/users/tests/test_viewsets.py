"""
test for app users
"""
import json
import pytest
import datetime as dt
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from users.models import ApiUser,UserProfile, UserPermission	# pylint: disable=relative-beyond-top-level
from users.serializers import ApiUserSerializer, UserProfileSerializer, UserPermissionSerializer	# pylint: disable=relative-beyond-top-level
from users.viewsets import ApiUserViewSet, UserProfileViewSet, UserPermissionViewSet	# pylint: disable=relative-beyond-top-level

from users.models import Turn, Department, UserDepartment	# pylint: disable=relative-beyond-top-level
from users.serializers import TurnSerializer, DepartmentSerializer, UserDepartmentSerializer	# pylint: disable=relative-beyond-top-level
from users.viewsets import TurnViewSet, DepartmentViewSet, UserDepartmentViewSet	# pylint: disable=relative-beyond-top-level

from permissions.models import Profile, Permission
from permissions.serializers import ProfileSerializer, PermissionSerializer
from permissions.viewsets import ProfileViewSet, PermissionViewSet

pytestmark = pytest.mark.django_db


class TestApiUserViewSet: #pylint: disable=too-few-public-methods
    """
    Test for ApiUserViewSet
    """

    @pytest.mark.urls('users.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('apiuser-list')

        data = {"username": 'test1', "password": "pass1", "email":"TEST_EMAIL@test.com"}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(ApiUser, 'save')
        # Renderizamos la vista con nuestro request.
        response = ApiUserViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == 201
        assert json.loads(response.content).get('email') == 'TEST_EMAIL@test.com'
        # Verificamos si efectivamente se llamo el metodo save
        assert ApiUser.save.called


class TestUserProfileViewSet: #pylint: disable=too-few-public-methods
    """
    Test for UserProfileViewSet
    """

    @pytest.mark.urls('permissions.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('profilepermission-list')

        profile_test = Profile()
        profile_test.name="profile_test_viewset"
        profile_test.key="test"
        profile_test.description="test"
        profile_test.save()


        user_test = ApiUser()
        user_test.username="test1"
        user_test.password="pass1"
        user_test.email="TEST_EMAIL@test.com"
        user_test.save()

        data = {"profile":profile_test.id, "user": user_test.id}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(UserProfile, 'save')
        # Renderizamos la vista con nuestro request.
        response = UserProfileViewSet.as_view({'post': 'create'})(request).render()
        profile = Profile.objects.get(id = json.loads(response.content).get('profile') )
        assert response.status_code == 201
        assert str(profile) == 'profile_test_viewset'
        # Verificamos si efectivamente se llamo el metodo save
        assert UserProfile.save.called


class TestUserPermissionViewSet: #pylint: disable=too-few-public-methods
    """
    Test for UserPermissionViewSet
    """

    @pytest.mark.urls('permissions.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('profilepermission-list')

        permission_test = Permission()
        permission_test.name="user_permission_viewset"
        permission_test.key="test"
        permission_test.description="test"
        permission_test.save()

        user_test = ApiUser()
        user_test.username="test1"
        user_test.password="pass1"
        user_test.email="TEST_EMAIL@test.com"
        user_test.save()

        data = {"permission":permission_test.id, "user": user_test.id}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(UserPermission, 'save')
        # Renderizamos la vista con nuestro request.
        response = UserPermissionViewSet.as_view({'post': 'create'})(request).render()
        permission = Permission.objects.get(id = json.loads(response.content).get('permission') )
        assert response.status_code == 201
        assert str(permission) == 'user_permission_viewset'
        # Verificamos si efectivamente se llamo el metodo save
        assert UserPermission.save.called


class TestTurnViewSet: #pylint: disable=too-few-public-methods
    """
    Test for TurnViewSet
    """

    @pytest.mark.urls('users.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('turn-list')

        name = "turn_test"
        start_time = str(dt.datetime.strptime("07:00", '%H:%M').time())
        end_time = str(dt.datetime.strptime("12:00", '%H:%M').time())

        data = {"name": name, "start_time": start_time, "end_time":end_time}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(Turn, 'save')
        # Renderizamos la vista con nuestro request.
        response = TurnViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == 201
        assert json.loads(response.content).get('name') == 'turn_test'
        # Verificamos si efectivamente se llamo el metodo save
        assert Turn.save.called


class TestDepartmentViewSet: #pylint: disable=too-few-public-methods
    """
    Test for DepartmentViewSet
    """

    @pytest.mark.urls('users.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('department-list')

        name = "department_test"

        data = {"name": name}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(Department, 'save')
        # Renderizamos la vista con nuestro request.
        response = DepartmentViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == 201
        assert json.loads(response.content).get('name') == 'department_test'
        # Verificamos si efectivamente se llamo el metodo save
        assert Department.save.called


class TestUserDepartmentViewSet: #pylint: disable=too-few-public-methods
    """
    Test for UserDepartmentViewSet
    """

    @pytest.mark.urls('users.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('userdepartment-list')
        #user
        #department
        #turn
        user_test = ApiUser()
        user_test.username="test1"
        user_test.password="pass1"
        user_test.email="TEST_EMAIL@test.com"
        user_test.save()

        department_test = Department()
        department_test.name = "department_test_v"
        department_test.save()

        turn_test = Turn()
        turn_test.name = "turn_test_v"
        turn_test.description = "Description"
        turn_test.start_time = dt.datetime.strptime("08:00", '%H:%M').time()
        turn_test.end_time = dt.datetime.strptime("15:00", '%H:%M').time()
        turn_test.save()

        data = {"user":user_test.id, "department": department_test.id, "turn": turn_test.id, 'manager': True}


        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(UserDepartment, 'save')
        # Renderizamos la vista con nuestro request.
        response = UserDepartmentViewSet.as_view({'post': 'create'})(request).render()
        department = Department.objects.get(id = json.loads(response.content).get('department') )
        turn = Turn.objects.get(id = json.loads(response.content).get('turn') )
        user = ApiUser.objects.get(id = json.loads(response.content).get('user') )
        manager = json.loads(response.content).get('manager')
        assert response.status_code == 201
        assert str(department) == 'department_test_v'
        assert str(turn) == 'turn_test_v'
        assert str(user.username) == 'test1'
        assert manager == True
        # Verificamos si efectivamente se llamo el metodo save
        assert UserDepartment.save.called