# -*- encoding: utf-8 -*-
"""
Autogenerate urls file
"""
from rest_framework.routers import DefaultRouter
from .viewsets import ApiUserViewSet, UserProfileViewSet, UserPermissionViewSet, AuthViewSet, DepartmentViewSet, TurnViewSet, UserDepartmentViewSet # pylint: disable=relative-beyond-top-level


router = DefaultRouter()
router.register(r'auth', AuthViewSet)
router.register(r'data', ApiUserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'permissions', UserPermissionViewSet)
router.register(r'turn', TurnViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'user-department', UserDepartmentViewSet)

urlpatterns = router.urls
