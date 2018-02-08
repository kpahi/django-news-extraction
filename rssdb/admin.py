from django.contrib import admin

from .models import rssdata

# Register your models here.


# admin.site.register(rssdata)


@admin.register(rssdata)
class RssAdmin(admin.ModelAdmin):
    list_display = ('location', 'death_no', 'injury_no',
                    'date', 'day', 'vehicle_number')

    search_fields = ['body']

    def vehicle_number(self, obj):
        all_vehicle = obj.vehicle_no

        k = [key for key, value in all_vehicle.items()]

        return ("%s" % (k))

    vehicle_number.short_description = 'Accident Vehicles'
