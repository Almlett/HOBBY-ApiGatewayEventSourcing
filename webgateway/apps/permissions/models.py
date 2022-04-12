"""
Models
"""
from django.utils.translation import ugettext_lazy as _
from django.db import models
from apigateway.models import Api

class Permission(models.Model):
    """
    Model Permission
    """
    TYPE_CHOICE_LIST  = (
        (0, _('Undefined')),
        (1, _('Get')),
        (2, _('List')),
        (3, _('Post')),
        (4, _('Put')),
        (5, _('Patch')),
        (6, _('Delete')),
        (7, _('Component')),
    )
    
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=100)
    description = models.TextField()
    enabled = models.BooleanField(default=True)
    api = models.ForeignKey(Api, on_delete=models.CASCADE, null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICE_LIST, default=0)

    class Meta:
        unique_together = ('name', 'key',)

    def __str__(self):
        """
        return name from model
        """
        return str(self.name)

class Profile(models.Model):
    """
    Model Profile
    """
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=100)
    description = models.TextField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        """
        return name from model
        """
        return str(self.name)

class ProfilePermission(models.Model):
    """
    Model ProfilePermission
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        """
        return name from model
        """
        return str(self.profile.name)