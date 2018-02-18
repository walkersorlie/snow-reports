#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen
from resorts.models import Resort_Weather, Resort
import datetime
import urllib2



"""
Alta scraper
"""

htmlfile = urllib2.Request('https://www.alta.com/conditions/daily-mountain-report/snow-report', headers = {'User-Agent': 'Mozilla/5.0'})
html = urlopen(htmlfile).read()
soup = BeautifulSoup(html, "lxml")
with open('alta.html', 'w') as file:
    file.write(html)

# with open("alta.html") as fp:
#     soup = BeautifulSoup(fp, "lxml")

# snow_report = soup.find(id = "snow-report")
# tables = snow_report.find_all("table", limit = 3)
tables = soup.find_all("table", class_ = "table table-weather", limit = 3)
article_id = soup.find("article", id = "snow-report")

# the Resort_Weather model fields
time = article_id.find("p", class_ = "text-right")
# print time.get_text(strip=True)
# response.write((time.get_text(strip=True) + " "))

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

# Resort_Weather model | CHANGE PK
# alta_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
# alta_weather.save()



"""
Snowbird scraper
"""

htmlfile = urllib2.Request('https://www.snowbird.com/mountain-report/', headers = {'User-Agent': 'Mozilla/5.0'})
html = urlopen(htmlfile).read()
soup = BeautifulSoup(html, "lxml")

with open('snowbird.html', 'w') as file:
    file.write(html)

# with open("snowbird.html") as fp:
#     soup = BeautifulSoup(fp, "lxml")

tables = soup.find_all('div', class_ = 'sb-condition_value', limit = 9)
time = soup.find('div', class_ = 'date-display')
forecast_tables = soup.find_all('div', class_ = 'swiper-wrapper', limit = 3)

# the Resort_Weather model fields
last_updated_date = datetime.datetime.today()

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

# Resort_Weather model | CHANGE PK
snowbird_weather = Resort_Weather(last_updated=last_updated_date, last_updated_time=last_updated_time_field, twelve_hour_snow=twelve_hour_snow_field, twenty4_hour_snow=twenty4_hour_snow_field, base=base_field, total_snow=total_snow_field, current_temp=current_temp_field, current_weather=current_weather_field, forecast=forecast_field, resort=foreign_key)
snowbird_weather.save()
