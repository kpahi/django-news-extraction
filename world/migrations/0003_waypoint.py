# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 08:56
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_auto_20170525_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='WayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]