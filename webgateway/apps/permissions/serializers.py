"""
Autogenerate serializers file
"""
from rest_framework import serializers
from .models import Permission, Profile, ProfilePermission	# pylint: disable=relative-beyond-top-level

class PermissionSerializer(serializers.ModelSerializer):
    """
    Permission Serialzier
    """
    api_showtext = serializers.SerializerMethodField()
    type_showtext = serializers.SerializerMethodField()

    class Meta: 	# pylint: disable=too-few-public-methods
        """
        Select all fields from model Permission
        """

        model = Permission
        fields = "__all__"
    
    
    def get_api_showtext(self, obj):
        if not obj.api:
            return '-'
        return obj.api.api_path

    def get_type_showtext(self, obj):
        return obj.get_type_display()

  

class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile Serialzier
    """
    permit_list = serializers.SerializerMethodField()

    class Meta: 	# pylint: disable=too-few-public-methods
        """
        Select all fields from model Profile
        """

        model = Profile
        fields = '__all__'
    
    def get_permit_list(self, obj):
        profile_permission = ProfilePermission.objects.filter(profile = obj)
        result = []
        for item in profile_permission:
            data = {}
            data['permission'] = PermissionSerializer(item.permission, many=False).data
            data['enabled'] = item.enabled
            result.append(data)
        print (result)
        return result

class ProfilePermissionSerializer(serializers.ModelSerializer):
    """
    ProfilePermission Serialzier
    """

    class Meta: 	# pylint: disable=too-few-public-methods
        """
        Select all fields from model ProfilePermission
        """

        model = ProfilePermission
        fields = '__all__'