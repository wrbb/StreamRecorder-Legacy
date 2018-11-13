# Stream Recorder

These scripts are used to recording each show based on the Spinitron schedule and move the recording to given storage location and place the file within a folder of the shows name. The script works but using Spinitron's API to get the list of the shows and applescript events along with Nicecasts recording feature to start and stop recording the shows and shell scripts to move the files to the given location.

## Overview

The process works as follows: First `apiAccess.py` should be run. This script makes a request to the Spinitron API that returns a list of the shows on the current schedule and their end times. The script then goes through each shows and creates a [Cron job](https://en.wikipedia.org/wiki/Cron) for each show that tells it run `stop_recording_and_store.sh` at each shows end time and passes along to that script the name of the show. It also will create a cronjob to run the `apiAccess.py` script every night at midnight to update the shows being recorded in case of a change in the schedule or for when shows are changed every semester.

Next, `stop_recording_and_store.sh` is run automatically due to the cron jobs. This script, given the name of the show, will either 1. If Nicecast is not currently recording, press the record button and begin recording or 2. If Nicecast is recording, press the stop recording button and move the recording file Nicecast produces to the storage location set in the script inside a folder with the same name as the show just recorded (if the folder does not exist it will be created). It then will press the recording button again before exiting.

## How each script works

### apiAccess.py

This script uses the spinitron API link for shows and our API access token to recieve a JSON for each show which contains a ton of info about each show (start time, id, end time, name, duration etc). Our script only uses the name and end time to create the cron job. It parses the given end time to get the hour and day of the week it ends and creates a cron job in the following way

```
[end minute] [end hour] * * [day of week] /location/of/stop_recording_and_store.sh "[name of show]"
```

It then writes all the cron jobs created for each show to a file called cronfile and finally adds 

```
"0 0 * * * /opt/wrbb-spinitron/apiAccess.py"
```

As the last time so that the script is run every night at midnight. 

It then clears all previous cronjobs stored in cron and writes all jobs in cronfile to cron


### notfiy.sh

This script simply uses slack's url requests to send a message (given as command line argument 0) as the Vortex slack bot

### isRecording.sh

This script uses applescript to commands to simply print out the label on the Nicecast recording button. Either 'Stop Archiving' if Nicecast is currently recording or 'Start Archiving' if Nicecast is not recording.

### stop_recording_and_store.sh

The script is what is called by the cron jobs created by `apiAccess.py`. This script takes in the name of the show to record and checks if it is recording using the `isRecording` script and does 1 of two things. 1. If Nicecast is not recording yet, start recording by using an applescript to click the `Start Archiving` button and record the current date and time in a file (This is explained below). The other thing it will do, if it is already recording, stop the recording by using an applescript to press the `Stop Archiving` button and then move the file from the default output location for Nicecast to `/[Specified recording location]/[Given Show name]/[Current Date].mp3`. It finally starts the recording again and recording the date and time.

#### Why it records the date when starting recording

Every time it starts a recording it records the `[Year][Month][Day] [Hour][Minute]` in a temp file because when Nicecast stops recording, the name of the default output is in the same format, so when stopping the recording, to know which file you want it simply gets the contents of the temp file.
