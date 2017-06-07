from django.contrib.postgres.fields import JSONField
from django.db import models


# Create your models here.


class News(models.Model):
    body = models.TextField(blank=False, null=False)
    death = models.CharField(blank=True, max_length=100)
    injury = models.CharField(blank=True, max_length=100)
    location = models.CharField(blank=True, max_length=100)
    #vehicle_no = models.CharField(blank=True, max_length=100)
    vehicle_no = JSONField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'Newss'

    def __str__(self):
        return self.location
