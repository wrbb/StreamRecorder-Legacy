#!/bin/bash 
# Sends a notification to the slackbot to have it say which show it stopped recording and where the recording was placed in the "vortexupdates" channel

echo "$1"
data='{"text": "'$1'"}' 
echo $data

curl -X POST \
  --header "Content-Type: application/json" \
  --data "$data" \
  https://hooks.slack.com/services/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

