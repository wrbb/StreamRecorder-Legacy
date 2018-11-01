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

def get_datetime(timestr):
    return datetime.datetime.strptime(timestr[:-5], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=-4)
def get_day_of_week(timestr):
    return get_datetime(timestr).isoweekday() % 7

STORE_LOCATION = '/opt/wrbb-spinitron/storage'

cronfile = open('cronfile', 'w')

response = urllib2.urlopen('https://spinitron.com/api/shows?access-token=ARdWnef9Fie7lKWspQzn5efv&count=1000')
data = json.load(response)
results = data["items"]

shows = [] 
for show in results:
    ashow = {}
    ashow['name'] = show["title"]
    ashow["id"] = show["id"]
    ashow["offAir"] = show["end"]
    ashow["onAir"] = show["start"]
    starttime = get_datetime(ashow['onAir'])
    endtime = get_datetime(ashow['offAir'])
    ashow['onAirDatetime'] = starttime
    ashow["endh"] = endtime.hour
    ashow["endm"] = endtime.minute
    ashow["totaltime"] = show['duration']
    shows.append(ashow)
    #print "Added show {}".format(ashow['name'].encode('utf-8'))


for show in shows:
    time = get_datetime(show['onAir'])
    namenospace = re.sub('[#*/!,.& \:\' ]','', show["name"]) 
    
    cronfile.write("%s %s * * %s /opt/wrbb-spinitron/stop_recording_and_store.sh" % (show["endm"], show["endh"], get_day_of_week(show['onAir'])))
    cronfile.write(' "{}" '.format(namenospace.encode("utf-8")))
    cronfile.write(STORE_LOCATION)
    cronfile.write('\n')


cronfile.write("0 0 * * * /opt/wrbb-spinitron/apiAccess.py\n")
cronfile.close()
subprocess.call(["crontab", "-r"])
subprocess.call("crontab cronfile", shell=True)
