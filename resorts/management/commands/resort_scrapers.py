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

        solitude_thread = ScraperThread('solitude')
        solitude_thread.start()

        alta_thread.join()
        snowbird_thread.join()
        brighton_thread.join()
        solitude_thread.join()


        """
        urls = [
        'https://www.alta.com/conditions/daily-mountain-report/snow-report',
        'https://www.snowbird.com/mountain-report/',
        'http://www.brightonresort.com/mountain/snow-report/',
        'https://solitudemountain.com/on-the-mountain'
        ]
        # Make the Pool of workers
        pool = ThreadPool(4)
        # Open the urls in their own threads
        # and return the results
        results = pool.map(urllib2.urlopen, urls)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()
        print results[0]

        """


class ScraperThread(Thread):

    ''' Constructor. '''
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

def alta():
    """
    Alta scraper
    """

    htmlfile = urllib2.Request('https://www.alta.com/conditions/daily-mountain-report/snow-report', headers = {'User-Agent': 'Mozilla/5.0'})
    html = urlopen(htmlfile).read()
    soup = BeautifulSoup(html, "lxml")
    # with open('/home/walker/senior_proj/snow_site/reports/alta.html', 'w') as file:
    #     file.write(html)

    # with open("./reports/alta.html") as fp:
    #     soup = BeautifulSoup(fp, "lxml")

    # snow_report = soup.find(id = "snow-report")
    # tables = snow_report.find_all("table", limit = 3)
    tables = soup.find_all("table", class_ = "table table-weather", limit = 3)
    article_id = soup.find("article", id = "snow-report")

    # the Resort_Weather model fields
    time = article_id.find("p", class_ = "text-right")
    # print time.get_text(strip=True)
    # response.write((time.get_text(strip=True) + " "))

    # last_updated_date = datetime.datetime.today()
    # last_updated_date = localtime(now())
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
            # There is a seperate div that has this info as well
            for specific, row in enumerate(entries):
                if specific == 0:   # twelve_hour_snow
                    # response.write(row)
                    # twelve_hour_snow_field = str(row.find('td'))
                    twelve_hour_snow_field = row.find('td').get_text()
                    # response.write((twelve_hour_snow_field + "<br><br>"))
                elif specific == 1: # twenty4_hour_snow_field
                    # response.write(row)
                    # twenty4_hour_snow_field = str(row.find('td'))
                    twenty4_hour_snow_field = row.find('td').get_text()
                    # response.write((twenty4_hour_snow_field + "<br><br>"))
                elif specific == 3: # base_field
                    # base_field = str(row.find('td'))
                    base_field = row.find('td').get_text()
                    # print base_field
                    # response.write((base_field + "<br><br>"))
                elif specific == 4: # total_snow_field
                    # total_snow_field = str(row.find('td')) + " "
                    total_snow_field = row.find('td').get_text()
                    # response.write((total_snow_field + "<br><br>"))
        elif count == 1:  # current_weather
            for specific, row in enumerate(entries):
                if specific == 0:   # sky coverage
                    # response.write(row)
                    table_rows = row.find_all('td')
                    # current_weather_field = str(table_rows[1])
                    current_weather_field = table_rows[1].get_text()
                    # response.write(current_weather)
                elif specific == 1: # winds
                    table_rows = row.find_all('td')
                    # current_weather_field = current_weather_field + str(table_rows[0]) + str(table_rows[1])
                    current_weather_field = current_weather_field + table_rows[0].get_text() + table_rows[1].get_text()
                    # response.write((current_weather_field + "<br><br>"))
                elif specific == 2: # temperature
                    # current_temp_field = str(row.find('td'))
                    current_temp_field = row.find('td').get_text()
                    # response.write((current_temp_field + "<br><br>"))
        elif count == 2:   # forecast
            for specific, row in enumerate(entries):
                if specific == 0:   # sky cover
                    table_rows = row.find_all('td')
                    # forecast_field = forecast_field + str(table_rows[1])
                    forecast_field = forecast_field + "Sky cover: " + table_rows[1].get_text() + " "
                    # response.write(forecast_field)
                elif specific == 1: # winds
                    table_rows = row.find_all('td')
                    forecast_field = forecast_field + "Winds: " + table_rows[0].get_text() + table_rows[1].get_text() + " "
                    # response.write(forecast_field)
                elif specific == 2: # high temp range
                    table_rows = row.find('td')
                    forecast_field = forecast_field + "High temperature range: " + table_rows.get_text() + " "
                    # response.write(forecast_field)
                elif specific == 3: # expected snwofall
                    table_rows = row.find('td')
                    forecast_field = forecast_field + "Expected snowfall: " + table_rows.get_text()
                    # response.write(forecast_field)

    # Resort_Weather model
    alta_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    alta_weather.save()

def snowbird():
    """
    Snowbird scraper
    """

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
    # last_updated_date = localtime(now())

    last_updated_time_field = time.get_text()
    # response.write(last_updated_time_field + "<br><br>")

    twelve_hour_snow_field = tables[0].get_text()
    # response.write(twelve_hour_snow_field + "<br><br>")

    twenty4_hour_snow_field = tables[1].get_text()
    # response.write(twenty4_hour_snow_field + "<br><br>")

    base_field = tables[3].get_text()
    # response.write(base_field + "<br><br>")

    total_snow_field = tables[4].get_text()
    # response.write(total_snow_field + "<br><br>")

    current_temp_field = tables[6].get_text()
    # response.write(current_temp_field + "<br><br>")

    current_weather_field = tables[8].get_text()
    # response.write(current_weather_field + "<br><br>")

    forecast_field = ""
    foreign_key = Resort.objects.get(pk=2)

    for count, table in enumerate(forecast_tables):
        if count == 0:
            forecast_field = table.find('div', class_ = 'description').get_text()
            # response.write(forecast_field)

    # Resort_Weather model
    snowbird_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    snowbird_weather.save()

def brighton():
    """
    Brighton scraper
    """

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
    # last_updated_date = localtime(now())
    last_updated_time_field = ""
    twelve_hour_snow_field = current_snow.find('h2').get_text()
    twenty4_hour_snow_field = ""
    # base_field = snow_totals.find('h2').get_text()
    base_field = snow_totals.find('p').get_text()
    total_snow_field = ""
    current_temp_field = current_temp.find('h2').get_text()
    current_weather_field = current_temp.find('p').get_text()
    forecast_field = forecast.find('p').get_text()
    foreign_key = Resort.objects.get(pk=3)

    # print twelve_hour_snow_field
    # print base_field
    # print total_snow_field
    # print current_temp_field
    # print current_weather_field
    # print forecast_field

    # Resort_Weather model
    brighton_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    brighton_weather.save()

def solitude():
    """
    Solitude scraper
    """

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
    #snow_totals = snow_totals_outer.find_all('div', class_='item')
    weather_details_outer = weather_tables.find('div', class_='weather-details')
    weather_details = weather_details_outer.find('ul').find_all('li')

    last_updated_date = datetime.datetime.now()
    # last_updated_date = localtime(now())
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

    # print last_updated_time_field
    # print twenty4_hour_snow_field
    # print base_field
    # print total_snow_field
    # print current_temp_field
    # print current_weather_field

    # Resort_Weather model
    solitude_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
    solitude_weather.save()

    # print "script ran at: " + datetime.datetime.now()
