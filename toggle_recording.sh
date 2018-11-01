
# This script will toggle the nicecast recording 
# (osascript that sends cmd+r to nicecast)

osascript -e 'activate application "Nicecast"'
osascript -e 'tell application "System Events"' -e 'keystroke "r" using command down' -e 'end tell'
