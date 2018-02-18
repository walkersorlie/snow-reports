#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup, NavigableString
from urllib2 import urlopen
from resort.models import UAAC_Report
import datetime
import urllib2



"""
UAAC scraper
"""

htmlfile = urllib2.Request('https://utahavalanchecenter.org/advisory/salt-lake', headers = {'User-Agent': 'Mozilla/5.0'})
html = urlopen(htmlfile).read()
soup = BeautifulSoup(html, "lxml")

with open('uaac.html', 'w') as file:
  file.write(html)

# with open("uaac.html") as fp:
#     soup = BeautifulSoup(fp, "lxml")

avalanche_problems = soup.find_all('div', class_ = 'clearbg avalanche-problem-row')

issued_by = soup.find(id = "subtitle-date-row")
area_field = issued_by.find('th').get_text()
forcaster_field = issued_by.find('td').get_text()

advisory_field = soup.find(id = "problem-rose")
advisory_field = advisory_field.find('p').get_text()

current_conditions_field = soup.find(id = "current-conditions-row")
# current_conditions_field = current_conditions_field.find('span').get_text() + current_conditions_field.find('p').get_text()
current_conditions_field = current_conditions_field.find('p').get_text()

# recent_activity = soup.find(id = "recent-activity-row")
# response.write(recent_activity.find('span'))
# response.write(recent_activity.find('p'))

weather_field = soup.find(id = "weather-row")
weather_field = weather_field.find('p').get_text()

# UAAC_Report model
# uaac_report = UAAC_Report(area=area_field, forcaster=forcaster_field, date=datetime.datetime.today(), advisory=advisory_field, current_conditions=current_conditions_field, weather=weather_field)
# uaac_report.save()

print "It worked!!!"
