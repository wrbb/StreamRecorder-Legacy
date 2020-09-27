#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import sys
import urllib2
import json
import time
import re
import subprocess
import datetime

# Returns the current date and time formated into [Year]-[Month]-[Day]T[Hour]:[Minute]:[Second]
def get_datetime(timestr):
    return datetime.datetime.strptime(timestr[:-5], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=-5)
# Gets the number the represents the day of the week (i.e. 0 = Sunday, 1 = Monday, ... , 6 = Saturday)
def get_day_of_week(timestr):
    return get_datetime(timestr).isoweekday() % 7

# The Location as to where to write the recordings to
#STORE_LOCATION = '/opt/wrbb-spinitron/storage'

# Opens a file called `cronfile` that will store the cronjobs 
cronfile = open('cronfile', 'w')

# Requests the schedule for shows from spinitron
response = urllib2.urlopen('https://spinitron.com/api/shows?access-token=ARdWnef9Fie7lKWspQzn5efv&count=1000')
# Loads the json data from the response
data = json.load(response)
# Gets the results from the requests (i.e. All the shows data, start end times etc)
results = data["items"]

shows = [] 
epoch = datetime.datetime(1970, 1, 1)
# Loops through each item in results (the shows)
# For each show, gets the name, id, start time, end time, and duration
# Adds that data to the shows array
for show in results:
    ashow = {}
    ashow['name'] = show["title"]
    ashow["id"] = show["id"]
    ashow["offAir"] = show["end"]
    ashow["onAir"] = show["start"]
    starttime = get_datetime(ashow['onAir'])
    endtime = get_datetime(ashow['offAir'])
    ashow['onAirDatetime'] = starttime
    ashow["starth"] = starttime.hour
    ashow["startm"] = starttime.minute
    ashow["timestamp"] = int((endtime - epoch).total_seconds())
    ashow["totaltime"] = show['duration']
    shows.append(ashow)
    #print "Added show {}".format(ashow['name'].encode('utf-8'))


# For each show, creates a cronjob that calls `stop_recording_and_store` at the shows end time with the name of the show and where to place the recording
for show in shows:
    time = get_datetime(show['onAir'])
    namenospace = re.sub('[#*/!,.& \:\' ]','', show["name"]) 
    
    cronfile.write("%s %s * * %s /opt/wrbb-spinitron/recordShow.py" % (show["startm"], show["starth"], get_day_of_week(show['onAir'])))
    cronfile.write(' "{}" '.format(namenospace.encode("utf-8")))
    cronfile.write(str(show['timestamp']))
    cronfile.write('\n')

# Then writes this file to be run every night at midnight to update the show list, in case of any changes to the schedule
cronfile.write("0 0 * * * /opt/wrbb-spinitron/apiAccess.py\n")
# Closes the file
cronfile.close()
# Removes all cronjobs currently listed
subprocess.call(["crontab", "-r"])
# Adds all cron jobs in the cronfile
subprocess.call("crontab cronfile", shell=True)
