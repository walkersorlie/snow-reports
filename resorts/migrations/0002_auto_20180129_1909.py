# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-29 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort_weather',
            name='twelve_hour_snow',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='resort_weather',
            name='twenty4_hour_snow',
            field=models.CharField(max_length=25),
        ),
    ]
