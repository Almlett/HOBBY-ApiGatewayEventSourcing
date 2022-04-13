"""
Autogenerate admin file
"""
from django.contrib import admin
from .models import EndPoint, Api  # pylint: disable=relative-beyond-top-level


class EndPointAdmin(admin.ModelAdmin):
    """
    Add EndPoint to Admin
    """


class ApiAdmin(admin.ModelAdmin):
    """
    Add Api to Admin
    """


admin.site.register(EndPoint, EndPointAdmin)
admin.site.register(Api, ApiAdmin)
