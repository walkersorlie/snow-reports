# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from resorts.models import Resort_Weather, Resort, UAAC_Report
from datetime import datetime, timedelta


def get_last_three_days(resort_set, uaac):
    dates = []
    latest_records = []
    past_three_days = []

    if uaac == 'uaac':
        for day in resort_set:
            dates.append(day.date)
        # print dates
        # print
        latest = dates[0]
        for day in dates:
            if day.date() != latest.date():
                latest_records.append(latest)
                latest = day
            else:
                if day > latest:
                    latest = day

        for day in resort_set:
            if day.date in latest_records and len(past_three_days) < 3:
                day.date = day.date.date()
                past_three_days.append(day)
    else:
        for day in resort_set:
            dates.append(day.last_updated)
        # print dates
        # print
        latest = dates[0]
        for day in dates:
            if day.date() != latest.date():
                latest_records.append(latest)
                latest = day
            else:
                if day > latest:
                    latest = day

        for day in resort_set:
            if day.last_updated in latest_records and len(past_three_days) < 3:
                day.last_updated = day.last_updated.date()
                past_three_days.append(day)

    return reversed(past_three_days)

def index(request):
    context = {'response' : "Resorts homepage"}
    return render(request, 'resorts/index.html', context)

def alta(request):
    latest_alta_weather = Resort_Weather.objects.filter(resort__exact=1, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=1, last_updated__isnull=False).order_by('-last_updated')[1:12]
    reversed_past_three_days = get_last_three_days(past_three_days, '')
    # need to figure out how to get 3 days, not last 3 records
    # compare last_updated datetime to today's date -1???
    # OR get 3 records from yesterday, day before, and before day before
    # get latest report from each past day
    # get all reports from day before, then get latest record from that set???
    print reversed_past_three_days
    context = {'latest_alta_weather': latest_alta_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/alta.html', context)

def snowbird(request):
    latest_snowbird_weather = Resort_Weather.objects.filter(resort__exact=2, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=2, last_updated__isnull=False).order_by('-last_updated')[1:12]
    reversed_past_three_days = get_last_three_days(past_three_days, '')
    context = {'latest_snowbird_weather': latest_snowbird_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/snowbird.html', context)

def brighton(request):
    latest_brighton_weather = Resort_Weather.objects.filter(resort__exact=3, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=3, last_updated__isnull=False).order_by('-last_updated')[1:12]
    reversed_past_three_days = get_last_three_days(past_three_days, '')
    context = {'latest_brighton_weather': latest_brighton_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/brighton.html', context)

def solitude(request):
    latest_solitude_weather = Resort_Weather.objects.filter(resort__exact=4, last_updated__isnull=False).latest('last_updated')
    past_three_days = Resort_Weather.objects.filter(resort__exact=4, last_updated__isnull=False).order_by('-last_updated')[1:12]
    reversed_past_three_days = get_last_three_days(past_three_days, '')
    context = {'latest_solitude_weather': latest_solitude_weather,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/solitude.html', context)

def uaac(request):
    latest_uaac_report = UAAC_Report.objects.filter(date__isnull=False).latest('date')
    past_three_days = UAAC_Report.objects.filter(date__isnull=False).order_by('-date')[1:6]
    reversed_past_three_days = get_last_three_days(past_three_days, 'uaac')
    context = {'latest_uaac_report': latest_uaac_report,
                'past_three_days': reversed_past_three_days}
    return render(request, 'resorts/uaac.html', context)
