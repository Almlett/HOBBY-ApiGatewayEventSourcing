"""
test for app users
"""
import json
import pytest
import datetime as dt
from users.models import ApiUser,UserProfile, UserPermission, PasswordToken, Turn, Department, UserDepartment 	# pylint: disable=relative-beyond-top-level
from permissions.models import Profile, Permission

pytestmark = pytest.mark.django_db

class TestApiUser:
    """
    Test ApiUser Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, api_user_factory,):	# pylint: disable=no-self-use
        """
        test created apiuser
        """

        apiuser_created = api_user_factory()
        apiuser = ApiUser.objects.get(id = apiuser_created.id)
        assert apiuser.username == "user_test", 'UserName should be user_test'
        assert str(apiuser) == "user_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, api_user_factory,):	# pylint: disable=no-self-use
        """
        test updated apiuser
        """

        apiuser_created = api_user_factory()
        apiuser = ApiUser.objects.get(id = apiuser_created.id)

        apiuser.email = "test_email@email.com"
        apiuser.save()
        assert apiuser.email == "test_email@email.com", 'Email should be test_email@email.com'


class TestPasswordToken:
    """
    Test PasswordToken Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, password_token_factory,):	# pylint: disable=no-self-use
        """
        test created PasswordToken
        """

        PasswordToken_created = password_token_factory()
        passwordtoken = PasswordToken.objects.get(id = PasswordToken_created.id)
        assert passwordtoken.key == "key_test", 'Key should be key_test'
        assert str(passwordtoken) == "key_test"


    pytestmark = pytest.mark.django_db
    def test_update(self, password_token_factory,):	# pylint: disable=no-self-use
        """
        test updated PasswordToken
        """

        PasswordToken_created = password_token_factory()
        passwordtoken = PasswordToken.objects.get(id = PasswordToken_created.id)

        passwordtoken.email = "test_email@email.com"
        passwordtoken.save()
        assert passwordtoken.email == "test_email@email.com", 'Email should be test_email@email.com'


class TestUserProfile:
    """
    Test UserProfile Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, user_profile_factory,):	# pylint: disable=no-self-use
        """
        test created user_profile
        """

        user_profile_created = user_profile_factory()
        user_profile = UserProfile.objects.get(id = user_profile_created.id)
        assert user_profile.profile.name == "profile_test", 'Name should be user_profile_test'
        assert str(user_profile) == "profile_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, user_profile_factory,):	# pylint: disable=no-self-use
        """
        test updated user_profile
        """
        profile_test = Profile()
        profile_test.name="user_profile_test2"
        profile_test.key="test"
        profile_test.description="test"
        profile_test.save()


        user_profile_created = user_profile_factory()
        user_profile = UserProfile.objects.get(id = user_profile_created.id)

        user_profile.profile = profile_test
        user_profile.save()

        assert user_profile.profile.name == "user_profile_test2", 'name should be user_profile_test2'

class TestUserPermission:
    """
    Test UserPermission Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, user_permission_factory,):	# pylint: disable=no-self-use
        """
        test created user_permission
        """

        user_permission_created = user_permission_factory()
        user_permission = UserPermission.objects.get(id = user_permission_created.id)
        assert user_permission.permission.name == "permission_test", 'Name should be user_permission_test'
        assert str(user_permission) == "permission_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, user_permission_factory,):	# pylint: disable=no-self-use
        """
        test updated user_permission
        """
        permission_test = Permission()
        permission_test.name="user_permission_test2"
        permission_test.key="test"
        permission_test.description="test"
        permission_test.save()


        user_permission_created = user_permission_factory()
        user_permission = UserPermission.objects.get(id = user_permission_created.id)

        user_permission.permission = permission_test
        user_permission.save()

        assert user_permission.permission.name == "user_permission_test2", 'name should be user_permission_test2'


class TestTurn:
    """
    Test Turn Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, turn_factory,):	# pylint: disable=no-self-use
        """
        test created turn
        """

        turn_created = turn_factory()
        turn = Turn.objects.get(id = turn_created.id)
        assert turn.name == "turn_test", 'Name should be turn_test'
        assert str(turn.start_time) == "07:00:00", 'Start time should be 07:00:00'
        assert str(turn.end_time) == "12:00:00", 'End time should be 12:00:00'
        assert str(turn) == "turn_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, turn_factory,):	# pylint: disable=no-self-use
        """
        test updated turn
        """
        
        turn_created = turn_factory()
        turn = Turn.objects.get(id = turn_created.id)
        turn.end_time = dt.datetime.strptime("13:00", '%H:%M').time()
        turn.save()

        assert str(turn.end_time) == "13:00:00", 'End time should be 13:00:00'


class TestDepartment:
    """
    Test Department Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, department_factory,):	# pylint: disable=no-self-use
        """
        test created department
        """

        department_created = department_factory()
        department = Department.objects.get(id = department_created.id)
        assert department.name == "department_test", 'Name should be department_test'
        assert str(department) == "department_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, department_factory,):	# pylint: disable=no-self-use
        """
        test updated department
        """
        
        department_created = department_factory()
        department = Department.objects.get(id = department_created.id)
        department.name = "department2"
        department.save()

        assert department.name == "department2", 'Name should be department2'


class TestUserDepartment:
    """
    Test UserDepartment Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, user_department_factory,):	# pylint: disable=no-self-use
        """
        test created user_department
        """

        user_department_created = user_department_factory()
        user_department = UserDepartment.objects.get(id = user_department_created.id)
        assert user_department.user.username == "user_test", 'Name should be user_test'
        assert user_department.department.name == "department_test", 'Name should be department_test'
        assert user_department.turn.name == "turn_test", 'Name should be turn_test'
        assert user_department.manager == True, 'Manager should be True'
        assert str(user_department) == 'department_test-user_test'

    pytestmark = pytest.mark.django_db
    def test_update(self, user_department_factory,):	# pylint: disable=no-self-use
        """
        test updated user_department
        """
        department_test = Department()
        department_test.name = "updated_department"
        department_test.general_profile = "General Profile 2"
        department_test.save()


        user_department_created = user_department_factory()
        user_department = UserDepartment.objects.get(id = user_department_created.id)

        user_department.department = department_test
        user_department.save()

        assert str(user_department.department.name) == "updated_department", 'End time should be updated_department'
