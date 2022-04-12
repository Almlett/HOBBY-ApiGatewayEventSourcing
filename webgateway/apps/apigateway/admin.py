"""
Autogenerate admin file
"""
from django.contrib import admin
from .models import Proyect, Api	# pylint: disable=relative-beyond-top-level


class ProyectAdmin(admin.ModelAdmin):
    """
    Add Proyect to Admin
    """


class ApiAdmin(admin.ModelAdmin):
    """
    Add Api to Admin
    """




admin.site.register(Proyect, ProyectAdmin)
admin.site.register(Api, ApiAdmin)
