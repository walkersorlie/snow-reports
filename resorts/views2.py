# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen
from resorts.models import Resort_Weather, Resort, UAAC_Report
import datetime
import urllib2


def index(request):
    context = {'response' : "Resorts homepage"}
    return render(request, 'resorts/index.html', context)
    # return HttpResponse("Resorts page")

def alta(request):
    response = HttpResponse()
    # htmlfile = urllib2.Request('https://www.alta.com/conditions/daily-mountain-report/snow-report', headers = {'User-Agent': 'Mozilla/5.0'})
    # html = urlopen(htmlfile).read()
    # soup = BeautifulSoup(html, "lxml")
    # with open('alta.html', 'w') as file:
    #     file.write(html)

    with open("alta.html") as fp:
        soup = BeautifulSoup(fp, "lxml")

    latest = Resort_Weather.objects.filter(resort__exact=1, date_time__isnull=False).latest('date_time')
    latest2 = Resort_Weather.objects.filter(resort__exact=2, date_time__isnull=False).latest('date_time')
    # latest = Resort_Weather.objects.get(resort__exact=1).latest('date_time')
    # print latest2
    # print latest.pk

    tables = soup.find_all("table", class_ = "table table-weather", limit = 3)
    article_id = soup.find("article", id = "snow-report")

    # the Resort_Weather model fields
    time = article_id.find("p", class_ = "text-right")
    last_updated_date = datetime.datetime.today()
    last_updated_time_field = time.get_text()
    twelve_hour_snow_field = ""
    twenty4_hour_snow_field = ""
    base_field = ""
    total_snow_field = ""
    current_temp_field = ""
    current_weather_field = ""
    forecast_field = ""
    foreign_key = Resort.objects.get(pk=1)

    response.write((time.get_text(strip=True) + " "))

    # set all the field variables
    for count, table in enumerate(tables):
        entries = table.find_all("tr")
        # snowfall
        if count == 0:
            # There is a seperate div that has this info as well
            for specific, row in enumerate(entries):
                # twelve_hour_snow
                if specific == 0:
                    twelve_hour_snow_field = row.find('td').get_text()
                    response.write((twelve_hour_snow_field + "<br><br>"))
                # twenty4_hour_snow_field
                elif specific == 1:
                    twenty4_hour_snow_field = row.find('td').get_text()
                    response.write((twenty4_hour_snow_field + "<br><br>"))
                # base_field
                elif specific == 3:
                    base_field = row.find('td').get_text()
                    response.write((base_field + "<br><br>"))
                # total_snow_field
                elif specific == 4:
                    total_snow_field = row.find('td').get_text()
                    response.write((total_snow_field + "<br><br>"))
        # current_weather
        elif count == 1:
            for specific, row in enumerate(entries):
                # sky coverage
                if specific == 0:
                    table_rows = row.find_all('td')
                    current_weather_field = table_rows[1].get_text()
                # winds
                elif specific == 1:
                    table_rows = row.find_all('td')
                    current_weather_field = current_weather_field + table_rows[0].get_text() + table_rows[1].get_text()
                    response.write((current_weather_field + "<br><br>"))
                # temperature
                elif specific == 2:
                    current_temp_field = row.find('td').get_text()
                    response.write((current_temp_field + "<br><br>"))
        # forecast
        elif count == 2:
            for specific, row in enumerate(entries):
                # sky cover
                if specific == 0:
                    table_rows = row.find_all('td')
                    forecast_field = forecast_field + "Sky cover: " + table_rows[1].get_text() + " "
                # winds
                elif specific == 1:
                    table_rows = row.find_all('td')
                    forecast_field = forecast_field + "Winds: " + table_rows[0].get_text() + table_rows[1].get_text() + " "
                # high temp range
                elif specific == 2:
                    table_rows = row.find('td')
                    forecast_field = forecast_field + "High temperature range: " + table_rows.get_text() + " "
                # expected snwofall
                elif specific == 3:
                    table_rows = row.find('td')
                    forecast_field = forecast_field + "Expected snowfall: " + table_rows.get_text()
                    response.write(forecast_field)

    return response

def snowbird(request):
    response = HttpResponse()
    # htmlfile = urllib2.Request('https://www.snowbird.com/mountain-report/', headers = {'User-Agent': 'Mozilla/5.0'})
    # html = urlopen(htmlfile).read()
    # soup = BeautifulSoup(html, "lxml")
    #
    # with open('snowbird.html', 'w') as file:
    #     file.write(html)

    with open("snowbird.html") as fp:
        soup = BeautifulSoup(fp, "lxml")

    tables = soup.find_all('div', class_ = 'sb-condition_value', limit = 9)
    time = soup.find('div', class_ = 'date-display')
    forecast_tables = soup.find_all('div', class_ = 'swiper-wrapper', limit = 3)

    # the Resort_Weather model fields
    last_updated_date = datetime.datetime.today()

    last_updated_time_field = time.get_text()
    response.write(last_updated_time_field + "<br><br>")

    twelve_hour_snow_field = tables[0].get_text()
    response.write(twelve_hour_snow_field + "<br><br>")

    twenty4_hour_snow_field = tables[1].get_text()
    response.write(twenty4_hour_snow_field + "<br><br>")

    base_field = tables[3].get_text()
    response.write(base_field + "<br><br>")

    total_snow_field = tables[4].get_text()
    response.write(total_snow_field + "<br><br>")

    current_temp_field = tables[6].get_text()
    response.write(current_temp_field + "<br><br>")

    current_weather_field = tables[8].get_text()
    response.write(current_weather_field + "<br><br>")

    forecast_field = ""
    foreign_key = Resort.objects.get(pk=2)

    for count, table in enumerate(forecast_tables):
        if count == 0:
            forecast_field = table.find('div', class_ = 'description').get_text()
            response.write(forecast_field)

    # Resort_Weather model | CHANGE PK
    snowbird_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    snowbird_weather.save()

    return response

def uaac(request):
    response = HttpResponse()
    # htmlfile = urllib2.Request('https://utahavalanchecenter.org/advisory/salt-lake', headers = {'User-Agent': 'Mozilla/5.0'})
    # html = urlopen(htmlfile).read()
    # soup = BeautifulSoup(html, "lxml")
    #
    # with open('uaac.html', 'w') as file:
    #     file.write(html)

    with open("uaac.html") as fp:
        soup = BeautifulSoup(fp, "lxml")

    avalanche_problems = soup.find_all('div', class_ = 'clearbg avalanche-problem-row')

    issued_by = soup.find(id = "subtitle-date-row")
    area_field = issued_by.find('th').get_text()
    forcaster_field = issued_by.find('td').get_text()
    response.write(area_field + "<br><br>")
    response.write(forcaster_field + "<br><br>")
    # response.write((issued_by.get_text() + "<br><br>"))

    advisory_field = soup.find(id = "problem-rose")
    advisory_field = advisory_field.find('p').get_text()
    # strong = advisory_field.find_all('strong')

    # response.write((advisory_field.find('p').get_text() + "<br><br>"))
    response.write(advisory_field + "<br><br>")

    current_conditions_field = soup.find(id = "current-conditions-row")
    # current_conditions_field = current_conditions_field.find('span').get_text() + current_conditions_field.find('p').get_text()
    current_conditions_field = current_conditions_field.find('p').get_text()
    # response.write((current_conditions_field.find('span').get_text() + "<br><br>"))
    # response.write((current_conditions_field.find('p').get_text() + "<br><br>"))
    response.write(current_conditions_field + "<br><br>")

    # recent_activity = soup.find(id = "recent-activity-row")
    # response.write(recent_activity.find('span'))
    # response.write(recent_activity.find('p'))

    weather_field = soup.find(id = "weather-row")
    weather_field = weather_field.find('p').get_text()
    # response.write((weather_field.find('span').get_text() + "<br><br>"))
    # response.write((weather_field.find('p').get_text() + "<br><br>"))
    response.write(weather_field + "<br><br>")

    # UAAC_Report model
    uaac_report = UAAC_Report(area=area_field, forcaster=forcaster_field, date=datetime.datetime.today(), advisory=advisory_field, current_conditions=current_conditions_field, weather=weather_field)
    uaac_report.save()

    return response
