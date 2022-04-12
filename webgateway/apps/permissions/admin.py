"""
Autogenerate admin file
"""
from django.contrib import admin
from .models import Permission, Profile, ProfilePermission	# pylint: disable=relative-beyond-top-level


class PermissionAdmin(admin.ModelAdmin):
    """
    Add Permission to Admin
    """

class ProfileAdmin(admin.ModelAdmin):
    """
    Add Profile to Admin
    """

class ProfilePermissionAdmin(admin.ModelAdmin):
    """
    Add ProfilePermission to Admin
    """

admin.site.register(Permission, PermissionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfilePermission, ProfilePermissionAdmin)
