#!/bin/bash 

echo "$1"
data='{"text": "'$1'"}' 
echo $data

curl -X POST \
  --header "Content-Type: application/json" \
  --data "$data" \
  https://hooks.slack.com/services/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

