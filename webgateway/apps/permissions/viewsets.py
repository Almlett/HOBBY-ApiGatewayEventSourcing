"""
Autogenerate viewsets file
"""
from rest_framework import viewsets
from .models import Permission, Profile, ProfilePermission 	# pylint: disable=relative-beyond-top-level
from .serializers import PermissionSerializer, ProfileSerializer, ProfilePermissionSerializer # pylint: disable=relative-beyond-top-level

class PermissionViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    Permission ViewSet
    """

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class ProfileViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    Profile ViewSet
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfilePermissionViewSet(viewsets.ModelViewSet):	# pylint: disable=too-many-ancestors
    """
    ProfilePermission ViewSet
    """

    queryset = ProfilePermission.objects.all()
    serializer_class = ProfilePermissionSerializer

