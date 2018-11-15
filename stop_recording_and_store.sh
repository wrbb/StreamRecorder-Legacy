#!/bin/bash

# Location of where Nicecast will place the recordings when finished
recording_location="/Users/stream/Music/Nicecast Broadcast Archive/Nicecast Archived Audio"
# The location of where the recordings should be placed
storage_location="/Volumes/untitled/Shows"
# The previous time of the recoding (used to identify the file finished recording)
file_name_recorder="$HOME/.file_time"
# The show name passed as an arugument to the script
show_name="$1"

# Runs `isRecording` and echos the output
function is_recording {
    echo $(/opt/wrbb-spinitron/isRecording)
}

# Press the start and stop recording button by using an applescript
function press_start_stop {
    osascript -e "tell application \"System Events\" 
    tell process \"Nicecast\"
        click menu item \"$1\" of menu \"Control\" of menu bar 1
    end tell
end tell"
}

# Moves a file
function move_file {
    # If driectory for the show is not present in the sotrage location, make one
    mkdir -p "$storage_location/$(echo $show_name)/"
    # Gets the name of the file that Nicecast produces
    recording_file=$recording_location\ $(cat $file_name_recorder).mp3
    # Gets the name of the file to move the recording file to
    storage_file=$storage_location/$(echo $show_name)/$(echo $show_name)_$(date +%m-%d-%Y).mp3
    # Send notification via slackbot
    /opt/wrbb-spinitron/notify.sh "Move $recording_file to $storage_file"
    # Move the Nicecast recording file to the storage location
    mv "$recording_file" "$storage_file"

}

# If Nicecast is recording, stop and move the file to the storage location
if [ "$(is_recording)" = "Stop Archiving" ]; then
    # Presses the stop recording
    press_start_stop "$(is_recording)"

    sleep 1 
    # Move the file
    move_file

    sleep 1
    # Presses start recording
    press_start_stop "Start Archiving"
    # Records the time started recording (Usefull because nicecast will name the output file with the time started)
    date +%Y%m%d\ %H%M > $file_name_recorder
else
    # If Nice cast is not recording, start recording and record time
    press_start_stop "$(is_recording)"
    date +%Y%m%d\ %H%M > $file_name_recorder
fi

