# Django build-in
from django.contrib.gis.db import models

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

    def __str__(self):
        return f"Description:{self.description} - {self.created} - state:{self.status} "
