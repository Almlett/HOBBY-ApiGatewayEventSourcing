"""
test for app users
"""
import json
import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from permissions.models import Permission, Profile, ProfilePermission	# pylint: disable=relative-beyond-top-level
from permissions.serializers import PermissionSerializer, ProfileSerializer, ProfilePermissionSerializer	# pylint: disable=relative-beyond-top-level
from permissions.viewsets import PermissionViewSet, ProfileViewSet, ProfilePermissionViewSet	# pylint: disable=relative-beyond-top-level

pytestmark = pytest.mark.django_db

class TestPermissionViewSet: #pylint: disable=too-few-public-methods
    """
    Test for PermissionViewSet
    """

    @pytest.mark.urls('permissions.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('permission-list')

        data = {"name": 'permission_test', "key": "permission_key", "description": "descripion text"}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(Permission, 'save')
        # Renderizamos la vista con nuestro request.
        response = PermissionViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == 201
        assert json.loads(response.content).get('name') == 'permission_test'
        # Verificamos si efectivamente se llamo el metodo save
        assert Permission.save.called


class TestProfileViewSet: #pylint: disable=too-few-public-methods
    """
    Test for ProfileViewSet
    """

    @pytest.mark.urls('permissions.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('profile-list')

        data = {"name": 'profile_test', "key": "profile_key", "description": "descripion text"}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(Profile, 'save')
        # Renderizamos la vista con nuestro request.
        response = ProfileViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == 201
        assert json.loads(response.content).get('name') == 'profile_test'
        # Verificamos si efectivamente se llamo el metodo save
        assert Profile.save.called

class TestProfilePermissionViewSet: #pylint: disable=too-few-public-methods
    """
    Test for ProfilePermissionViewSet
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

        permission_test = Permission()
        permission_test.name="permission_test_viewset"
        permission_test.key="test"
        permission_test.description="test"
        permission_test.save()

        data = {"profile":profile_test.id, "permission": permission_test.id}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(ProfilePermission, 'save')
        # Renderizamos la vista con nuestro request.
        response = ProfilePermissionViewSet.as_view({'post': 'create'})(request).render()
        print(response.content)
        profile = Profile.objects.get(id = json.loads(response.content).get('profile') )
        assert response.status_code == 201
        assert str(profile) == 'profile_test_viewset'
        # Verificamos si efectivamente se llamo el metodo save
        assert ProfilePermission.save.called