# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-06 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0002_auto_20180129_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resort_weather',
            name='base',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='resort_weather',
            name='current_temp',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='resort_weather',
            name='total_snow',
            field=models.CharField(max_length=25),
        ),
    ]