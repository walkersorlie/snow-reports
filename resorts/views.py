# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from resorts.models import Resort_Weather, Resort, UAAC_Report


def index(request):
    context = {'response' : "Resorts homepage"}
    return render(request, 'resorts/index.html', context)

def alta(request):
    latest_alta_weather = Resort_Weather.objects.filter(resort__exact=1, last_updated__isnull=False).latest('last_updated')
    context = {'latest_alta_weather': latest_alta_weather}
    return render(request, 'resorts/alta.html', context)

def snowbird(request):
    latest_snowbird_weather = Resort_Weather.objects.filter(resort__exact=2, last_updated__isnull=False).latest('last_updated')
    print latest_snowbird_weather
    context = {'latest_snowbird_weather': latest_snowbird_weather}
    return render(request, 'resorts/snowbird.html', context)

def brighton(request):
    latest_brighton_weather = Resort_Weather.objects.filter(resort__exact=3, last_updated__isnull=False).latest('last_updated')
    print latest_brighton_weather
    context = {'latest_brighton_weather': latest_brighton_weather}
    return render(request, 'resorts/brighton.html', context)

def solitude(request):
    latest_solitude_weather = Resort_Weather.objects.filter(resort__exact=4, last_updated__isnull=False).latest('last_updated')
    print latest_solitude_weather
    context = {'latest_solitude_weather': latest_solitude_weather}
    return render(request, 'resorts/solitude.html', context)

def uaac(request):
    latest_uaac_report = UAAC_Report.objects.filter(date__isnull=False).latest('date')
    context = {'latest_uaac_report': latest_uaac_report}
    return render(request, 'resorts/uaac.html', context)
