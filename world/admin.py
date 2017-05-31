from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin

from .models import WayPoint, WorldBorder

# Register your models here.

admin.site.register(WorldBorder, GeoModelAdmin)
admin.site.register(WayPoint)
