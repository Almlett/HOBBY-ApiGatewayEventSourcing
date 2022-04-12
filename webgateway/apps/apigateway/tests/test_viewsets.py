"""
test for app users
"""
import json
import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from apigateway.models import Proyect, Api	# pylint: disable=relative-beyond-top-level
from apigateway.serializers import ProyectSerializer, ApiSerializer	# pylint: disable=relative-beyond-top-level
from apigateway.viewsets import ProyectViewSet, ApiViewSet	# pylint: disable=relative-beyond-top-level

pytestmark = pytest.mark.django_db

class TestProyectViewSet: #pylint: disable=too-few-public-methods
    """
    Test for ProyectViewSet
    """

    @pytest.mark.urls('apigateway.urls')
    def test_get(self, rf, mocker):	# pylint: disable=no-self-use disable=invalid-name
        """
        test create
        """
        url = reverse('proyect-list')

        data = {"name": 'test1', "host": "host1", "port":8001}

        request = rf.post(url,
                          content_type='application/json',
                          data=json.dumps(data))

        mocker.patch.object(Proyect, 'save')
        # Renderizamos la vista con nuestro request.
        response = ProyectViewSet.as_view({'post': 'create'})(request).render()
        assert response.status_code == 201
        assert json.loads(response.content).get('host') == 'host1'
        # Verificamos si efectivamente se llamo el metodo save
        assert Proyect.save.called
