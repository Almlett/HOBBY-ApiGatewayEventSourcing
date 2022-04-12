"""
Confest
"""
import pytest
from pytest_factoryboy import register
from .factories import ApiUserFactory, UserPermissionFactory, UserProfileFactory, PasswordTokenFactory, TurnFactory, DepartmentFactory, UserDepartmentFactory	# pylint: disable=relative-beyond-top-level

register(ApiUserFactory)
register(UserPermissionFactory)
register(UserProfileFactory)
register(PasswordTokenFactory)
register(TurnFactory)
register(DepartmentFactory)
register(UserDepartmentFactory)

@pytest.fixture()
def post(api_user_factory,):
    """
    return fixture to use in tests
    """
    return api_user_factory,()

@pytest.fixture()
def post(password_token_factory,):
    """
    return fixture to use in tests
    """
    return password_token_factory,()

@pytest.fixture()
def post(user_permission_factory,):
    """
    return fixture to use in tests
    """
    return user_permission_factory,()

@pytest.fixture()
def post(user_profile_factory,):
    """
    return fixture to use in tests
    """
    return user_profile_factory,()

@pytest.fixture()
def post(turn_factory,):
    """
    return fixture to use in tests
    """
    return turn_factory,()

@pytest.fixture()
def post(department_factory,):
    """
    return fixture to use in tests
    """
    return department_factory,()


@pytest.fixture()
def post(user_department_factory,):
    """
    return fixture to use in tests
    """
    return user_department_factory,()
