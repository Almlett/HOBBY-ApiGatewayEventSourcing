# -*- encoding: utf-8 -*-
"""
"""

from django.conf.urls import include, re_path, url
from rest_framework.routers import DefaultRouter
from .viewsets import ProyectViewSet, ApiViewSet, Gateway  # pylint: disable=relative-beyond-top-level
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GATEWAY APIS",
        default_version='v0.0.1a',
        description="APIS of the Gateway",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'proyects', ProyectViewSet)
router.register(r'apilist', ApiViewSet)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
