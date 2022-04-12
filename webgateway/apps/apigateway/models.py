# -*- coding: utf-8 -*-
import requests, json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import get_authorization_header, BasicAuthentication
from rest_framework import HTTP_HEADER_ENCODING
    
#from users.utils import valid_token


class Proyect(models.Model):
    name = models.CharField(max_length=32)
    host = models.CharField(max_length=32)
    port = models.IntegerField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Api(models.Model):
    PLUGIN_CHOICE_LIST  = (
        (0, _('Remote auth')),
        (1, _('Token auth')),
    )
    api_path = models.CharField(max_length=128, unique=True)
    request_path = models.CharField(max_length=255)
    origin = models.ForeignKey(Proyect, on_delete = models.CASCADE)
    plugin = models.IntegerField(choices=PLUGIN_CHOICE_LIST, default=0)

    def __unicode__(self):
        return self.api_path

    def __str__(self):
        return self.api_path