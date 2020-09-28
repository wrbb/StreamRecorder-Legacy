#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time 
from datetime import date
import requests

today = date.today()

# dd/mm/YY
current_date = today.strftime("%d-%m-%Y")

# Location of show storage
SHOW_STORAGE="/Volumes/untitled/Shows"

# Show name
SHOW_NAME = sys.argv[1]
# show endtime
END_TIME = int(sys.argv[2])
 
stream_url = 'http://stream.radiojar.com/9950r946bzzuv'

r = requests.get(stream_url, stream=True)

os.makedirs(os.path.join(SHOW_STORAGE,SHOW_NAME))

with open(os.path.join(SHOW_STORAGE, SHOW_NAME, current_date + '.mp3'), 'wb') as f:
    for block in r.iter_content(1024):
        f.write(block)
        if time.time() > END_TIME:
            break
