# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from resorts.models import Resort_Weather, Resort, UAAC_Report


def index(request):
    context = {'response' : "Resorts homepage"}
    return render(request, 'resorts/index.html', context)

def alta(request):
    latest_alta_weather = Resort_Weather.objects.filter(resort__exact=1, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=1, last_updated__isnull=False).order_by('-last_updated')[:3]
    reversed_past_three_days = []
    for day in reversed(past_three_days):
        day.last_updated = day.last_updated.date()
        reversed_past_three_days.append(day)
    # need to figure out how to get 3 days, not last 3 records
    # compare last_updated datetime to today's date -1???
    # OR get 3 records from yesterday, day before, and day before before
    context = {'latest_alta_weather': latest_alta_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/alta.html', context)

def snowbird(request):
    latest_snowbird_weather = Resort_Weather.objects.filter(resort__exact=2, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=2, last_updated__isnull=False).order_by('-last_updated')[:3]
    reversed_past_three_days = []
    for day in reversed(past_three_days):
        day.last_updated = day.last_updated.date()
        reversed_past_three_days.append(day)
    # need to figure out how to get 3 days, not last 3 records
    # compare last_updated datetime to today's date -1???
    # OR get 3 records from yesterday, day before, and day before before
    context = {'latest_snowbird_weather': latest_snowbird_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/snowbird.html', context)

def brighton(request):
    latest_brighton_weather = Resort_Weather.objects.filter(resort__exact=3, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=3, last_updated__isnull=False).order_by('-last_updated')[:3]
    reversed_past_three_days = []
    for day in reversed(past_three_days):
        day.last_updated = day.last_updated.date()
        reversed_past_three_days.append(day)
    # need to figure out how to get 3 days, not last 3 records
    # compare last_updated datetime to today's date -1???
    # OR get 3 records from yesterday, day before, and day before before
    context = {'latest_brighton_weather': latest_brighton_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/brighton.html', context)

def solitude(request):
    latest_solitude_weather = Resort_Weather.objects.filter(resort__exact=4, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=4, last_updated__isnull=False).order_by('-last_updated')[:3]
    reversed_past_three_days = []
    for day in reversed(past_three_days):
        day.last_updated = day.last_updated.date()
        reversed_past_three_days.append(day)
    # need to figure out how to get 3 days, not last 3 records
    # compare last_updated datetime to today's date -1???
    # OR get 3 records from yesterday, day before, and day before before
    context = {'latest_solitude_weather': latest_solitude_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/solitude.html', context)

def uaac(request):
    latest_uaac_report = UAAC_Report.objects.filter(date__isnull=False).latest('date')
    past_three_days = UAAC_Report.objects.filter(date__isnull=False).order_by('-date')[:3]
    reversed_past_three_days = []
    for day in reversed(past_three_days):
        day.date = day.date.date()
        reversed_past_three_days.append(day)
    context = {'latest_uaac_report': latest_uaac_report,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/uaac.html', context)
