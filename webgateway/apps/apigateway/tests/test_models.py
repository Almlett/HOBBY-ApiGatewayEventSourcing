"""
test for app users
"""
import json
import pytest
from apigateway.models import Proyect, Api	# pylint: disable=relative-beyond-top-level

pytestmark = pytest.mark.django_db

class TestProyect:
    """
    Test Proyect Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, proyect_factory,):	# pylint: disable=no-self-use
        """
        test created proyect
        """

        proyect_created = proyect_factory()
        proyect = Proyect.objects.get(id = proyect_created.id)
        assert proyect.name == "name_test", 'Name should be name_test'
        assert str(proyect) == "name_test"

    pytestmark = pytest.mark.django_db
    def test_update(self, proyect_factory,):	# pylint: disable=no-self-use
        """
        test updated proyect
        """

        proyect_created = proyect_factory()
        proyect = Proyect.objects.get(id = proyect_created.id)

        proyect.host = 8004
        proyect.save()
        assert proyect.host == 8004, 'Host should be 8003'


class TestApi:
    """
    Test Api Model
    """

    pytestmark = pytest.mark.django_db
    def test_creation(self, api_factory,):	# pylint: disable=no-self-use
        """
        test created Api
        """

        Api_created = api_factory()
        api = Api.objects.get(id = Api_created.id)
        assert api.api_path == "path_test", 'API Path should be path_test'
        assert str(api) == "path_test"


    pytestmark = pytest.mark.django_db
    def test_update(self, api_factory,):	# pylint: disable=no-self-use
        """
        test updated Api
        """

        Api_created = api_factory()
        api = Api.objects.get(id = Api_created.id)

        api.api_path = "path_test2"
        api.save()
        assert api.api_path == "path_test2", 'API Path should be path_test2'

