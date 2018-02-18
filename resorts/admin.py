# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Resort, Resort_Weather, UAAC_Report

admin.site.register(Resort)
admin.site.register(Resort_Weather)
admin.site.register(UAAC_Report)
