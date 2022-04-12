# -*- encoding: utf-8 -*-
"""
Autogenerate urls file
"""
from rest_framework.routers import DefaultRouter
from .viewsets import PermissionViewSet, ProfileViewSet, ProfilePermissionViewSet # pylint: disable=relative-beyond-top-level

router = DefaultRouter()
router.register(r'list', PermissionViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'profileperms', ProfilePermissionViewSet)

urlpatterns = router.urls
