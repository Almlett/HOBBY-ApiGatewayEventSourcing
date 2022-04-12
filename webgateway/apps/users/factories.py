"""
Factories
"""
import factory
import datetime as dt
from faker import Factory as FakerFactory
from permissions.factories import PermissionFactory, ProfileFactory
from .models import ApiUser, UserPermission, UserProfile, PasswordToken, Turn, Department, UserDepartment	# pylint: disable=relative-beyond-top-level


faker = FakerFactory.create()


class ApiUserFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for ApiUser
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model ApiUser
        """
        model = ApiUser

    email = factory.LazyAttribute(lambda x: faker.email())	# pylint: disable=no-member
    username = "user_test"
    password = factory.LazyAttribute(lambda x: faker.password())	# pylint: disable=no-member


class PasswordTokenFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for PasswordToken
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model PasswordToken
        """
        model = PasswordToken

    user_email = factory.LazyAttribute(lambda x: faker.email())	# pylint: disable=no-member
    key = "key_test"


class UserPermissionFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for UserPermission
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model UserPermission
        """
        model = UserPermission

    user = factory.SubFactory(ApiUserFactory)	# pylint: disable=no-member
    permission = factory.SubFactory(PermissionFactory)	# pylint: disable=no-member


class UserProfileFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for UserProfile
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model UserProfile
        """
        model = UserProfile

    user = factory.SubFactory(ApiUserFactory)	# pylint: disable=no-member
    profile = factory.SubFactory(ProfileFactory)	# pylint: disable=no-member


class TurnFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for Turn
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model Turn
        """
        model = Turn

    
    name = "turn_test"
    start_time = dt.datetime.strptime("07:00", '%H:%M').time()
    end_time = dt.datetime.strptime("12:00", '%H:%M').time()


class DepartmentFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for Department
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model Department
        """
        model = Department

    
    name = "department_test"


class UserDepartmentFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for UserDepartment
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model UserDepartment
        """
        model = UserDepartment

    user = factory.SubFactory(ApiUserFactory)	# pylint: disable=no-member
    department = factory.SubFactory(DepartmentFactory)	# pylint: disable=no-member
    turn = factory.SubFactory(TurnFactory)	# pylint: disable=no-member
    manager = True
