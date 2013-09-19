#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Stephen Finucane

# Author: Stephen Finucane <stephenfinucane@hotmail.com>

from distutils.core import setup

setup(name='ul-ical-generator',
      version='0.1',
      description='University of Limerick timetable iCal file generator',
      author='Stephen Finucane',
      author_email='stephenfinucane@hotmail.com',
      packages=['ul-ical-generator'],
      install_requires=['requests', 'docopt', 'icalendar'],
     )