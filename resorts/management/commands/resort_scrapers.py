#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup, NavigableString
from django.core.management.base import BaseCommand, CommandError
from urllib2 import urlopen
from resorts.models import Resort_Weather, Resort
from django.utils.timezone import localtime, now
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
import datetime
import urllib2


class Command(BaseCommand):
    help = 'Runs the scrapers for the resorts'

    def handle(self, *args, **option):
        alta_thread = ScraperThread('alta')
        alta_thread.start()

        snowbird_thread = ScraperThread('snowbird')
        snowbird_thread.start()

        brighton_thread = ScraperThread('brighton')
        brighton_thread.start()

        # solitude_thread = ScraperThread('solitude')
        # solitude_thread.start()

        alta_thread.join()
        snowbird_thread.join()
        brighton_thread.join()
        # solitude_thread.join()

class ScraperThread(Thread):

    ''' Constructor '''
    def __init__(self, function):
        Thread.__init__(self)
        self.function = function

    def run(self):
        if self.function == 'alta':
            alta()
        elif self.function == 'snowbird':
            snowbird()
        elif self.function == 'brighton':
            brighton()
        else:
            solitude()

''' Alta Scraper '''
def alta():
    htmlfile = urllib2.Request('https://www.alta.com/conditions/daily-mountain-report/snow-report', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(htmlfile).read()
    soup = BeautifulSoup(html, "lxml")

    # with open('/home/walker/senior_proj/snow_site/reports/alta.html', 'w') as file:
    #     file.write(html)

    # with open("./reports/alta.html") as fp:
    #     soup = BeautifulSoup(fp, "lxml")

    tables = soup.find_all("table", class_ = "table table-weather", limit = 3)
    article_id = soup.find("article", id = "snow-report")

    # the Resort_Weather model fields
    time = article_id.find("p", class_ = "text-right")

    last_updated_date = datetime.datetime.now()
    last_updated_time_field = time.get_text()
    twelve_hour_snow_field = ""
    twenty4_hour_snow_field = ""
    base_field = ""
    total_snow_field = ""
    current_temp_field = ""
    current_weather_field = ""
    forecast_field = ""
    foreign_key = Resort.objects.get(pk=1)

    for count, table in enumerate(tables):
        entries = table.find_all("tr")
        if count == 0:  # snowfall
            for specific, row in enumerate(entries):
                if specific == 0:   # twelve_hour_snow
                    twelve_hour_snow_field = row.find('td').get_text()
                elif specific == 1: # twenty4_hour_snow_field
                    twenty4_hour_snow_field = row.find('td').get_text()
                elif specific == 2: # base_field
                    base_field = row.find('td').get_text()
                elif specific == 3: # total_snow_field
                    total_snow_field = row.find('td').get_text()
        elif count == 1:  # current_weather
            for specific, row in enumerate(entries):
                if specific == 0:   # sky coverage
                    table_rows = row.find_all('td')
                    current_weather_field = table_rows[1].get_text()
                elif specific == 1: # winds
                    table_rows = row.find_all('td')
                    current_weather_field = current_weather_field +", " + table_rows[0].get_text() + " " +  table_rows[1].get_text() + " wind"
                elif specific == 2: # temperature
                    current_temp_field = row.find('td').get_text()
        elif count == 2:   # forecast
            for specific, row in enumerate(entries):
                if specific == 0:   # sky cover
                    table_rows = row.find_all('td')
                    forecast_field = forecast_field + "Sky cover: " + table_rows[1].get_text() + "\n"
                elif specific == 1: # winds
                    table_rows = row.find_all('td')
                    forecast_field = forecast_field + "Winds: " + table_rows[0].get_text() + "/" +  table_rows[1].get_text() + "\n"
                elif specific == 2: # high temp range
                    table_rows = row.find('td')
                    forecast_field = forecast_field + "High temperature range: " + table_rows.get_text() + "\n"
                elif specific == 3: # expected snwofall
                    table_rows = row.find('td')
                    forecast_field = forecast_field + "Expected snowfall: " + table_rows.get_text()

    # Resort_Weather model
    alta_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    alta_weather.save()

''' Snowbird scraper'''
def snowbird():
    htmlfile = urllib2.Request('https://www.snowbird.com/mountain-report/', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(htmlfile).read()
    soup = BeautifulSoup(html, "lxml")

    # with open('/home/walker/senior_proj/snow_site/reports/snowbird.html', 'w') as file:
    #     file.write(html)

    # with open("./reports/snowbird.html") as fp:
    #     soup = BeautifulSoup(fp, "lxml")

    tables = soup.find_all('div', class_ = 'sb-condition_value', limit = 9)
    time = soup.find('div', class_ = 'date-display')
    forecast_tables = soup.find_all('div', class_ = 'swiper-wrapper', limit = 3)

    # the Resort_Weather model fields
    last_updated_date = datetime.datetime.today()
    last_updated_time_field = time.get_text()
    twelve_hour_snow_field = tables[0].get_text()
    twenty4_hour_snow_field = tables[1].get_text()
    base_field = tables[3].get_text()
    total_snow_field = tables[4].get_text()
    current_temp_field = tables[6].get_text()
    current_weather_field = tables[8].get_text()
    forecast_field = ""
    foreign_key = Resort.objects.get(pk=2)

    for count, table in enumerate(forecast_tables):
        if count == 0:
            forecast_field = table.find('div', class_ = 'description').get_text()

    # Resort_Weather model
    snowbird_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    snowbird_weather.save()

''' Brighton scraper '''
def brighton():
    htmlfile = urllib2.Request('http://www.brightonresort.com/mountain/snow-report/', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(htmlfile).read()
    soup = BeautifulSoup(html, "lxml")

    # with open('/home/walker/senior_proj/snow_site/reports/brighton.html', 'w') as file:
    #     file.write(html)

    # with open("./reports/brighton.html") as fp:
    #     soup = BeautifulSoup(fp, "lxml")

    current_weather_tables = soup.find('div', class_ = 'currently')

    current_temp = current_weather_tables.find('div', class_= 'c_info quarter')
    current_snow = current_weather_tables.find('div', class_='c_snow quarter')
    snow_totals = current_weather_tables.find('div', class_='c_totals quarter')
    forecast = soup.find('div', class_='extended_forecast')

    last_updated_date = datetime.datetime.now()
    last_updated_time_field = ""
    twelve_hour_snow_field = current_snow.find('h2').get_text()
    twenty4_hour_snow_field = ""
    base_field = snow_totals.find('p').get_text()
    total_snow_field = ""
    current_temp_field = current_temp.find('h2').get_text()
    current_weather_field = current_temp.find('p').get_text()
    forecast_field = ""
    foreign_key = Resort.objects.get(pk=3)

    # print forecast
    headers = forecast.find_all('h3', limit=3)
    content = forecast.find_all('p', limit=3)
    count = 0
    while count < 3:
        forecast_field = forecast_field + headers[count].get_text() + ": " + content[count].get_text() + " "
        count += 1

    # Resort_Weather model
    brighton_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    brighton_weather.save()

''' Solitude scraper '''
def solitude():
    htmlfile = urllib2.Request('https://solitudemountain.com/on-the-mountain', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(htmlfile).read()
    soup = BeautifulSoup(html, "lxml")

    # with open('/home/walker/senior_proj/snow_site/reports/solitude.html', 'w') as file:
    #     file.write(html)

    # with open("./reports/solitude.html") as fp:
    #     soup = BeautifulSoup(fp, "lxml")

    weather_tables = soup.find('div', class_='snow-details')
    current_weather_div = weather_tables.find('div', class_='current')
    snow_totals = weather_tables.find('div', class_='snow-totals').find_all('div', class_='item')
    weather_details_outer = weather_tables.find('div', class_='weather-details')
    weather_details = weather_details_outer.find('ul').find_all('li')

    forecast = soup.find('div', class_='wrap solitude-open').find('div', class_='item item-2')
    hilo = forecast.find('div', class_='hilo')

    last_updated_date = datetime.datetime.now()
    last_updated_time_field = ""
    twelve_hour_snow_field = ""
    twenty4_hour_snow_field = ""
    base_field = ""
    total_snow_field = ""
    current_temp_field = current_weather_div.find('div', class_='temp').get_text()
    current_weather_field = ""
    forecast_field = ""
    foreign_key = Resort.objects.get(pk=4)

    for count, div in enumerate(snow_totals):
        if count == 0:
            twenty4_hour_snow_field = div.find('span').get_text()
        elif count == 3:
            base_field = div.find('span').get_text()
        elif count == 4:
            total_snow_field = div.find('span').get_text()

    for count, li in enumerate(weather_details):
        if count == 0:
            last_updated_time_field = li.get_text()
        elif count == 3 or count == 4 or count == 5:
            current_weather_field = current_weather_field  + li.get_text() + " "

    for count, div in enumerate(hilo):
        if count == 0:
            temp = hilo.find('div', class_='high')
            forecast_field = forecast_field + "high: " + temp.find('span').get_text() + " "
        elif count ==1:
            temp = hilo.find('div', class_='low')
            forecast_field = forecast_field + "low: " + temp.find('span').get_text()

    # Resort_Weather model
    solitude_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    solitude_weather.save()
