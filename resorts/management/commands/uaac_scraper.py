#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup, NavigableString
from django.core.management.base import BaseCommand, CommandError
from urllib2 import urlopen
from resorts.models import UAAC_Report
from django.utils.timezone import localtime, now
import datetime
import urllib2


class Command(BaseCommand):
    help = 'Runs the scraper for the UAAC'

    """
    UAAC scraper
    """
    def handle(self, *args, **option):
        htmlfile = urllib2.Request('https://utahavalanchecenter.org/advisory/salt-lake', headers = {'User-Agent': 'Mozilla/5.0'})
        html = urlopen(htmlfile).read()
        soup = BeautifulSoup(html, "lxml")

        with open('/home/walker/senior_proj/snow_site/reports/uaac.html', 'w') as file:
          file.write(html)

        # with open("home/walker/senior_proj/snow_site/reports/uaac.html") as fp:
        #     soup = BeautifulSoup(fp, "lxml")

        avalanche_problems = soup.find_all('div', class_ = 'clearbg avalanche-problem-row')
        with open('/home/walker/senior_proj/snow_site/static/avi-problems.html', 'w') as file:
            # file.write("%s" % soup.head)
            # file.write("%s" % avalanche_problems)
            file.write(str(soup.head))
            file.write(str(avalanche_problems))

        # for table in avalanche_problems:
        #     problems_table = table.find('table', class_='avalanche-problem-table')
        #     print problems_table
        #     print
        #     for count, td in enumerate(problems_table):
        #         if count == 1:
        #             print td
        #             with open('/home/walker/senior_proj/snow_site/reports/avi-problems.html', 'w') as file:
        #               file.write(td)

        issued_by = soup.find(id = "subtitle-date-row")
        area_field = issued_by.find('th').get_text()
        forcaster_field = issued_by.find('td').get_text()

        advisory_field = soup.find(id = "problem-rose")
        advisory_field = advisory_field.find('p').get_text()

        current_conditions_field = soup.find(id = "current-conditions-row")
        current_conditions_field = current_conditions_field.find('p').get_text()

        # recent_activity = soup.find(id = "recent-activity-row")
        # response.write(recent_activity.find('span'))
        # response.write(recent_activity.find('p'))

        weather_field = soup.find(id = "weather-row")
        weather_field = weather_field.find('p').get_text()

        # UAAC_Report model
        uaac_report = UAAC_Report(area=area_field, forcaster=forcaster_field, date=datetime.datetime.now(), advisory=advisory_field, current_conditions=current_conditions_field, weather=weather_field)
        uaac_report.save()

        # self.stdout.write("It worked")
