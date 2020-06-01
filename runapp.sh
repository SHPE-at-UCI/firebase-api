#!/bin/sh

export FLASK_APP=app.py
export FLASK_ENV=development

#DEFAULTS
print=false

#size of buffer before trying to flush
export FLUSH_LIMIT=30

#time before flushing a non-empty buffer
export FLUSH_HOURS=1
export FLUSH_MINUTES=1

#copy of parameters
LIMIT=$FLUSH_LIMIT
HOURS=$FLUSH_HOURS
MINUTES=$FLUSH_MINUTES
#args=$(getopt -o "l:h:m:" -l "limit:,hours:,minutes:" -- "$@")
while getopts '?pl:h:m:' OPTION; do
  var=$(printf "%d\n" $OPTARG 2>/dev/null)
  case "$OPTION" in
    l)
        if [ $var -gt 0 ]; then
            LIMIT=$OPTARG
        fi;;
    h)
        if [ $var -gt 0 ]||[ $var -eq 0 ]&&[ $MINUTES != 0 ]; then
            HOURS=$OPTARG
        fi;;
    m)
        if [ $var -gt 0 ]||[ $var -eq 0 ]&&[ $HOURS != 0 ]; then
            MINUTES=$OPTARG
        fi;;
    p)
        print=true;;
    ?)
        echo "Usage: $0 [-?] [-p] [-l size] [-h hours] [-m minutes]"
        echo "Run flask app $FLASK_APP in $FLASK_ENV environment."
        echo ""
        echo "Current defaults are:"
        echo "  FLUSH_LIMIT   = $FLUSH_LIMIT"
        echo "  FLUSH_HOURS   = $FLUSH_HOURS"
        echo "  FLUSH_MINUTES = $FLUSH_MINUTES"
        echo ""
        echo "Options:"
        echo "  -? \t\t display this help and exit"
        echo "  -p \t\t print out values of parameters before running"
        echo "  -l size \t change how much data is needed before buffer flushing (>=1)"
        echo "  -h hours \t flush the buffer every so hours (>=0)"
        echo "  -m minutes \t flush the buffer every so minutes (>=0)"
        exit 0;;
  esac
done
#write back out parameters
$FLUSH_LIMIT=$LIMIT
$FLUSH_HOURS=$HOURS
$FLUSH_MINUTES=$MINUTES

if $print; then
    echo " Flush size limit: $FLUSH_LIMIT"
    echo " Reflush every $FLUSH_HOURS hour(s) $FLUSH_MINUTES minute(s)"
    echo ""
fi

flask run
