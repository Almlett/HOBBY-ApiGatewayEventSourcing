"""
Autogenerate serializers file
"""
from rest_framework import serializers
from .models import Proyect, Api	# pylint: disable=relative-beyond-top-level
from permissions.models import Permission


class ProyectSerializer(serializers.ModelSerializer):
    """
    Proyect Serialzier
    """

    class Meta: 	# pylint: disable=too-few-public-methods
        """
        Select all fields from model Proyect
        """

        model = Proyect
        fields = '__all__'

class ApiSerializer(serializers.ModelSerializer):
    """
    Api Serialzier
    """

    class Meta: 	# pylint: disable=too-few-public-methods
        """
        Select all fields from model Api
        """

        model = Api
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        TYPE_CHOICE_LIST  = [{'id':1, 'type':'GET'},
            {'id':2, 'type':'LIST'},
            {'id':3, 'type':'POST'},
            {'id':4, 'type':'PUT'},
            {'id':5, 'type':'PATCH'},
            {'id':6, 'type':'DELETE'}
        ]
        for item in TYPE_CHOICE_LIST:
            item_id = item['id']
            item_type = item['type']
            permission = Permission()
            permission.name = "{} | {} | {}".format(item_type, instance.origin.name, instance.api_path)
            permission.key = "{}{}{}".format(item_type.lower(), instance.origin.host, instance.api_path)
            permission.description = "Autogenerate permission type {} for {} from {}:{}".format(item_type, instance.api_path, instance.origin.name, instance.origin.port)
            permission.type = item_id
            permission.api = instance
            permission.save()
        return instance
