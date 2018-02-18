# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from resorts.models import Resort

class Resort_Weather(models.Model):
    last_updated = models.DateField()
    last_updated_time = models.CharField(max_length = 200)
    twelve_hour_snow = models.CharField(max_length = 25)
    twenty4_hour_snow = models.CharField(max_length = 25)
    base = models.CharField(max_length = 25)
    total_snow = models.CharField(max_length = 25)
    current_temp = models.CharField(max_length = 25)
    current_weather = models.TextField()
    forecast = models.TextField()
    resort = models.ForeignKey(Resort, on_delete = models.CASCADE)

    def __str__(self):
        return self.resort.name
    # Snowbird - http://forecast.weather.gov/MapClick.php?lat=40.58200000000005&lon=-111.65617999999995
    # Alta - http://forecast.weather.gov/MapClick.php?site=slc&smap=1&textField1=40.584583333333&textField2=-111.62125#.VQs510bwO1w
    # weather = Resort_Weather(last_updated=datetime.date.today(), last_updated_time="Last updated today at 6:00 pm", twelve_hour_snow=0, twenty4_hour_snow=1, base=65,total_snow=144, current_temp=21, current_weather="Partly sunny", forecast="Mostly sunny, with a high near 41. East wind 5 to 7 mph becoming light and variable", resort=1)
    # weather = Resort_Weather(last_updated=datetime.date.today(), last_updated_time="Last updated: 5:18 pm", twelve_hour_snow=0, twenty4_hour_snow=0,base=65, total_snow=159, current_temp=27, current_weather="Partly cloudy", forecast="Partly cloudy", resort=resort)
    # resort1 = Resort(name='Alta', location='Little Cottonwood Canyon')

class UAAC_Report(models.Model):
    # last_updated = models.CharField(max_length = 30)
    area = models.CharField(max_length = 100)
    forcaster = models.CharField(max_length = 100)
    date = models.DateField()
    advisory = models.TextField()
    current_conditions = models.TextField()
    weather = models.TextField()

    def __str__(self):
        return "UAAC Weather"
