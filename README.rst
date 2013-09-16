::

        _             _                 __ _       
       | |           | |               / _(_)      
    ___| |_ ___ _ __ | |__   ___ _ __ | |_ _ _ __  
   / __| __/ _ \ '_ \| '_ \ / _ \ '_ \|  _| | '_ \ 
   \__ \ ||  __/ |_) | | | |  __/ | | | | | | | | |
   |___/\__\___| .__/|_| |_|\___|_| |_|_| |_|_| |_|
               | |                                 
               |_|


What's ul-ical-generator?
=========================

ul-ical-generator is a python application for generating an ical file using the ul-rest-api_ datasources currently hosted on appspot_

.. _ul_rest_api: https://github.com/stephenfin/ul-rest-api
.. _appspot: http://ul-rest-api.appspot.com

Currently it provides no command line interface (the ID code is hard coded) and may have issues as a result of the beta status of the ul-rest-api API. 

How to use?
===========

Currently the app is not packaged. It can be run by calling the main.py script in the `ul-rest-api` folder. Don't forget to modify the ID number found in the call to `retrieve_timetable()`

Installation
============

Currently the app is not packaged. It can be run by calling the main.py script in the `ul-rest-api` folder. Don't forget to modify the ID number found in the call to `retrieve_timetable()`

Contribute
==========

Feel free to contribute towards any of the plans outlined below

Future Plans
============
  
  - Implement CLI
  - Implement GUI
  - Host as application on Google App Engine