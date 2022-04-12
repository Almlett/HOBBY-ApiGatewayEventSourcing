"""
test for app users
"""
import json
import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from apigateway.models import Proyect, Api	# pylint: disable=relative-beyond-top-level
from apigateway.serializers import ProyectSerializer, ApiSerializer	# pylint: disable=relative-beyond-top-level


pytestmark = pytest.mark.django_db


class TestProyectSerializer:
    """
    Test for ProyectSerializer
    """

    def test_expected_serialized_json(self,proyect_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        proyect_created = proyect_factory()
        proyect = Proyect.objects.get(id = proyect_created.id)
        results = ProyectSerializer(proyect).data

        assert results['name'] == "name_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
            'host':8006
        }

        serializer = ProyectSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestApiSerializer:
    """
    Test for ApiSerializer
    """

    def test_expected_serialized_json(self,api_factory):	# pylint: disable=no-self-use
        """
        test expected serialized json
        """
        api_created = api_factory()
        api = Api.objects.get(id = api_created.id)
        results = ApiSerializer(api).data
        assert results['api_path'] == "path_test"

    def test_raise_error_when_missing_required_field(self):	# pylint: disable=no-self-use
        """
        test raise error when missing required field
        """
        incomplete_data = {
            'id':1,
        }

        serializer = ApiSerializer(data=incomplete_data)

        # Este ContextManager nos permite verificar que
        # se ejecute correctamente una Excepcion
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

