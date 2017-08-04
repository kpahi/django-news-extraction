from datetime import date

from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class News(models.Model):
    # title = models.CharField(blank=True, max_length=100, null=True)
    body = models.TextField(blank=False, null=False)
    death = models.CharField(blank=True, max_length=100)
    death_no = models.IntegerField(blank=True, null=True)
    injury = models.CharField(blank=True, max_length=100)
    injury_no = models.IntegerField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100)
    vehicle_no = models.CharField(blank=True, max_length=100)
    vehicle_no = JSONField()
    date = models.DateField(default=date.today)
    slug = models.SlugField()
    day = models.CharField(blank=True, max_length=100)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'Newss'
        ordering = ('-date', 'location')

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.date) + "-" + (self.location))
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.slug
