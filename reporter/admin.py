# Register your models here.

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import PlacePoints


@admin.register(PlacePoints)
class LocationAdmin(OSMGeoAdmin):
    pass
