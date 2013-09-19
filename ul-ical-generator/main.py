#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

""" ul-ical-generator.

Usage:
  main.py <id_number>
  main.py <id_number> [-o <output_file>]
  main.py --version

Options:
  -h --help               Show this screen.
  -o FILE --output=FILE   Output file [default: ul_timetable.ics]
  --version               Show version.

"""

from __future__ import print_function

from icalendar import Calendar, Event
from datetime import datetime, timedelta
from dateutil import rrule
from docopt import docopt
from pytz import UTC

import collections
import requests
import json
import uuid

def generate_calendar(timetable, calendar):
  '''
  Generate a calendar file from the json data retrieved from the web service
  '''
  items = timetable['response']['data']['items']

  weekno_date = {}

  cal = Calendar()
  cal.add('prodid', '-//stephenfin//ul-rest-api.appspot.com//')
  cal.add('version', '2.0')
  cal.add('calscale', 'gregorian')
  cal.add('x-wr-calname', 'UL Calendar Sem 1 Year 2013')
  cal.add('x-wr-timezone', 'Europe/Dublin')
  cal.add('x-wr-caldesc', 'UL Academic Calendar for Current Year')

  print('Generating ical file using timetable and calendar')

  # generate list of "week number" - "date" tuples
  for (counter, date) in enumerate(rrule.rrule(rrule.WEEKLY, 
    dtstart=calendar[0], until=calendar[1])):
    weekno_date[str(counter + 1)] = date

  for day in items:
    for (counter, period) in enumerate(items[day]):
      # List of weeks module runs for in form [start, stop, start, stop]
      weeks = period['weeks']

      for index in range(0,len(weeks),2):
        # There may be no second range
        if weeks[index] is None:
          continue

        start_date = weekno_date[weeks[index]] + timedelta(days=int(day))
        end_date = (weekno_date[weeks[index + 1]] + 
          timedelta(days=int(day) + 1)).date()

        start_time = datetime.strptime(period['start_time'], '%H:%M').time()
        end_time = datetime.strptime(period['end_time'], '%H:%M').time()

        first_start = datetime.combine(start_date, start_time)
        first_end = datetime.combine(start_date, end_time)

        # google calendar complains if a UID is not specfied. Just generate 
        # randomness
        uid = '{0}@ul-rest-api.appspot.com'.format(uuid.uuid4())

        week_days = {
          0: "MO", 1: "TU", 2: "WE", 3: "TH", 4: "FR", 5: "SA",
        }

        # create an entry with an rrule
        event = Event()
        event.add('summary', '{0}: {1}'.format(period['module'], 
          period['period_type']))
        event.add('dtstart', first_start)
        event.add('dtend', first_end)
        event.add('rrule', {'freq': 'weekly', 'until': end_date, 
          'byday': week_days[int(day)]})
        event.add('dtstamp', datetime.now())
        event.add('uid', uid)
        event.add('created', datetime.now())
        event.add('location', period['room'])
        event.add('status', 'confirmed')

        # add to main calendar
        cal.add_component(event)

  return cal

def retrieve_timetable(id_number):
  '''
  Retrieve the timetable for a given student and converts it to a json object
  '''
  url = "http://ul-rest-api.appspot.com/api/v1/timetable"

  params = {
    'q' : id_number,
  }

  print('Getting timetable for student id {0}'.format(id_number))

  data = requests.get(url, params=params).text
  data = json.loads(data, object_pairs_hook=collections.OrderedDict)

  return data

def retrieve_calendar():
  '''
  Retrieve the timetable for a given student and converts it to a json object
  '''
  url = "http://ul-rest-api.appspot.com/api/v1/calendar"

  current_date = datetime.now()

  academic_year = current_date.strftime('%Y')

  # if into second semester we want to get the start year
  if current_date.month < 7:
    academic_year = str(int(academic_year) - 1)

  params = {
    'q' : academic_year,
  }

  print('Getting calendar for academic year starting Sept {0}'
    .format(academic_year))

  data = requests.get(url, params=params).text
  data = json.loads(data, object_pairs_hook=collections.OrderedDict)

  # If we're retrieving calendar before July, we want the spring semester dates
  if current_date.month < 7:
    start_date = data['response']['data']['items']['spring']['start']
    end_date = data['response']['data']['items']['spring']['end']
  else:
    start_date = data['response']['data']['items']['autumn']['start']
    end_date = data['response']['data']['items']['autumn']['end']

  start_date = datetime.strptime(start_date, "%a %d/%m/%Y").date()
  end_date = datetime.strptime(end_date, "%a %d/%m/%Y").date()

  return (start_date, end_date)

if __name__ == '__main__':
  args = docopt(__doc__)

  id_number = args['<id_number>']
  file_path = args['--output']

  print('Writing to file: {0}'.format(file_path))

  timetable = retrieve_timetable(id_number)
  calendar = retrieve_calendar()

  cal = generate_calendar(timetable, calendar)

  print('Writing ical to file')

  try:
    f = open(file_path, 'wb')
    f.write(cal.to_ical())
    f.close()
    print('Done')
  except:
    print('ERROR: There was an error writing to the file')