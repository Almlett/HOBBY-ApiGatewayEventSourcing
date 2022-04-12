"""
Confest
"""
import pytest
from pytest_factoryboy import register
from .factories import PermissionFactory, ProfileFactory, ProfilePermissionFactory	# pylint: disable=relative-beyond-top-level

register(PermissionFactory)
register(ProfileFactory)
register(ProfilePermissionFactory)

@pytest.fixture()
def post(permission_factory,):
    """
    return fixture to use in tests
    """
    return permission_factory,()


@pytest.fixture()
def post(profile_factory,):
    """
    return fixture to use in tests
    """
    return profile_factory,()

@pytest.fixture()
def post(profile_permission_factory,):
    """
    return fixture to use in tests
    """
    return profile_permission_factory,()