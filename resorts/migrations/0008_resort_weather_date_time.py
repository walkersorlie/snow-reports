# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-08 23:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resorts', '0007_auto_20180207_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort_weather',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 23, 54, 58, 868731)),
            preserve_default=False,
        ),
    ]