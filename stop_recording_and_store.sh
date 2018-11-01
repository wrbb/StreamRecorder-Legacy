#!/bin/bash


recording_location="/Users/stream/Music/Nicecast Broadcast Archive/Nicecast Archived Audio"
storage_location="/Volumes/untitled/Shows"
file_name_recorder="$HOME/.file_time"
show_name="$1"
echo $show_name

function is_recording {
    echo $(/opt/wrbb-spinitron/isRecording)
}

function press_start_stop {
    osascript -e "tell application \"System Events\" 
    tell process \"Nicecast\"
        click menu item \"$1\" of menu \"Control\" of menu bar 1
    end tell
end tell"
}

function move_file {
    mkdir -p "$storage_location/$(echo $show_name)/"
    recording_file=$recording_location\ $(cat $file_name_recorder).mp3
    storage_file=$storage_location/$(echo $show_name)/$(date +%m-%d-%Y).mp3
    /opt/wrbb-spinitron/notify.sh "Move $recording_file to $storage_file"
    mv "$recording_file" "$storage_file"

}

if [ "$(is_recording)" = "Stop Archiving" ]; then
    press_start_stop "$(is_recording)"
    sleep 1 
    move_file
    sleep 1
    press_start_stop "Start Archiving"
    date +%Y%m%d\ %H%M > $file_name_recorder
else
    press_start_stop "$(is_recording)"
    date +%Y%m%d\ %H%M > $file_name_recorder
fi

