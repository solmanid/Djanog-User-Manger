# Django build-in
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Third party
from guardian.models import (
    UserObjectPermissionBase,
    GroupObjectPermissionBase,
    UserObjectPermissionAbstract,
    GroupObjectPermissionAbstract
)
from guardian.shortcuts import assign_perm

# Local django
from accounts.models import User


# Create your models here.

class PlacePoints(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User"
    )

    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='upload/ed',
        verbose_name='Picture'
    )

    description = models.TextField(
        verbose_name='Description'
    )

    location = models.PointField(
        null=True,
        blank=True,
        verbose_name='Location'
    )

    likes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Likes'
    )

    status = models.BooleanField(
        default=True,
        verbose_name='Status'
    )

    created = models.DateField(
        auto_now_add=True,
        verbose_name='Created Time'
    )

    class Meta:
        default_permissions = ['add', 'change', 'delete', 'view']
        # permissions = (
        #     ('view_placepoints', 'Can view place points'),
        # )

    def __str__(self):
        return f"Description:{self.description} - {self.created} - state:{self.status} "


class PlacePointsUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(PlacePoints, on_delete=models.CASCADE)


class PlacePointsGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(PlacePoints, on_delete=models.CASCADE)


class BigUserObjectPermission(UserObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)

    class Meta(UserObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *UserObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'user']),
        ]


class BigGroupObjectPermission(GroupObjectPermissionAbstract):
    id = models.BigAutoField(editable=False, unique=True, primary_key=True)

    class Meta(GroupObjectPermissionAbstract.Meta):
        abstract = False
        indexes = [
            *GroupObjectPermissionAbstract.Meta.indexes,
            models.Index(fields=['content_type', 'object_pk', 'group']),
        ]


@receiver(post_save, sender=PlacePoints)
def set_permission(sender, instance: PlacePoints, **kwargs):
    assign_perm('view_placepoints', instance.user, instance)
    assign_perm('change_placepoints', instance.user, instance)
    assign_perm('delete_placepoints', instance.user, instance)

