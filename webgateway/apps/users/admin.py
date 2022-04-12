"""
Autogenerate admin file
"""
from django.contrib import admin
from .models import ApiUser, UserProfile, UserPermission, PasswordToken, UserDepartment, Department, Turn	# pylint: disable=relative-beyond-top-level


class ApiUserAdmin(admin.ModelAdmin):
    """
    Add ApiUser to Admin
    """


class UserProfileAdmin(admin.ModelAdmin):
    """
    Add UserProfile to Admin
    """


class UserPermissionAdmin(admin.ModelAdmin):
    """
    Add UserPermission to Admin
    """


class PasswordTokenAdmin(admin.ModelAdmin):
    """
    Add PasswordToken to Admin
    """


class TurnAdmin(admin.ModelAdmin):
    """
    Add Turn to Admin
    """


class DepartmentAdmin(admin.ModelAdmin):
    """
    Add Department to Admin
    """


class UserDepartmentAdmin(admin.ModelAdmin):
    """
    Add UserDepartment to Admin
    """


admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserPermission, UserPermissionAdmin)
admin.site.register(PasswordToken, PasswordTokenAdmin)
admin.site.register(Turn, TurnAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(UserDepartment, UserDepartmentAdmin)