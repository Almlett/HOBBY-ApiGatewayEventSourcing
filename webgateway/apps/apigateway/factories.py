"""
Factories
"""
import factory
from faker import Factory as FakerFactory
from .models import Proyect, Api	# pylint: disable=relative-beyond-top-level


faker = FakerFactory.create()


class ProyectFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for Proyect
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model Proyect
        """
        model = Proyect

    name = "name_test"
    host = factory.LazyAttribute(lambda x: faker.name())	# pylint: disable=no-member
    port = 8001	# pylint: disable=no-member


class ApiFactory(factory.django.DjangoModelFactory):
    """
    Default Factory for Api
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        Select Model Api
        """
        model = Api

    api_path = "path_test"
    request_path = factory.LazyAttribute(lambda x: faker.name())	# pylint: disable=no-member
    origin = factory.SubFactory(ProyectFactory)	# pylint: disable=no-member
    plugin = 0

