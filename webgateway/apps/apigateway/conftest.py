"""
Confest
"""
import pytest
from pytest_factoryboy import register
from .factories import ApiFactory, ProyectFactory	# pylint: disable=relative-beyond-top-level

register(ApiFactory)
register(ProyectFactory)

@pytest.fixture()
def post(api_factory,):
    """
    return fixture to use in tests
    """
    return api_factory,()

@pytest.fixture()
def post(proyect_factory,):
    """
    return fixture to use in tests
    """
    return proyect_factory,()
