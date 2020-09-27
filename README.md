# Stream Recorder

The WRBB Stream Recorder is a series of scripts to record shows from WRBB and make them internally available to the WRBB Staff for monitoring purposes. 

## Overview

The process works as follows: First `apiAccess.py` should be run. This script makes a request to the Spinitron API that returns a list of the shows on the current schedule and their end times. The script then goes through each shows and creates a [Cron job](https://en.wikipedia.org/wiki/Cron) for each show that tells it run `recordShow.py` at each shows start time and passes along to that script the name of the show and its end time in seconds since epoch. It also will create a cronjob to run the `apiAccess.py` script every night at midnight to update the shows being recorded in case of a change in the schedule or for when shows are changed every semester.

Next, when a show starts, the cronjob that `apiAccess.py` created is run, meaning the script `recordShow.py` is run, which begins writing the stream to an MP3 file in the shows folder in the storage drive. It continues to do this until the current time is greater than the time the show should end. It then exits the program.

## How each script works

### `apiAccess.py`

This script uses the spinitron API link for shows and our API access token to recieve a JSON for each show which contains a ton of info about each show (start time, id, end time, name, duration etc). Our script only uses the name and end time to create the cron job. It parses the given end time to get the hour and day of the week it ends and creates a cron job in the following way

```
[start minute] [start hour] * * [day of week] /location/of/recordShow.py "[name of show]" [ending time of show in seconds since epoch]
```

It then writes all the cron jobs created for each show to a file called cronfile and finally adds 

```
"0 0 * * * /opt/wrbb-spinitron/apiAccess.py"
```

As the last time so that the script is run every night at midnight. 

It then clears all previous cronjobs stored in cron and writes all jobs in cronfile to cron

## `recordShow.py`

This scirpt simply uses `requests` to continually write the stream to a file in the shows folder with the file name being the current date. It continually checks if the current time is greater than the end time of the show, and if it is (meaning the show is over) it exits the program
