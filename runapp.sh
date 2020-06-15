#!/bin/sh

#DEFAULTS
print=false

#flask variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_HOST=shpe.uci.edu

#size of buffer before trying to flush
export FLUSH_LIMIT=1

#time before flushing a non-empty buffer
export FLUSH_HOURS=1
export FLUSH_MINUTES=1


#copy of parameters
APP=$FLASK_APP
ENV=$FLASK_ENV
HOST=$FLASK_RUN_HOST
LIMIT=$FLUSH_LIMIT
HOURS=$FLUSH_HOURS
MINUTES=$FLUSH_MINUTES

while getopts '?pa:e:r:l:h:m:' OPTION; do
  var=$(printf "%d\n" $OPTARG 2>/dev/null)
  case "$OPTION" in
    a)
        if [ -f "$OPTARG" ]; then
            APP=$OPTARG
        fi;;
    e)
        if [ "$OPTARG" = "development" ]||[ "$OPTARG" = "production" ]; then
            ENV=$OPTARG
        fi;;
    r)
        if [ -n "$OPTARG" ]; then
            HOST=$OPTARG
        fi;;
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
        echo "Usage: $0 [-?] [-a app-name] [-e environ] [-r host-name] [-p] [-l size] [-h hours] [-m minutes]"
        echo "Run flask app '$FLASK_APP' in '$FLASK_ENV' environment with hostname '$FLASK_RUN_HOST' (by default)."
        echo ""
        echo "Current defaults are:"
        echo "  FLUSH_LIMIT   = $FLUSH_LIMIT"
        echo "  FLUSH_HOURS   = $FLUSH_HOURS"
        echo "  FLUSH_MINUTES = $FLUSH_MINUTES"
        echo ""
        echo "Options:"
        echo "  -? \t\t display this help and exit"
        echo "  -p \t\t print out values of parameters before running"
        echo "  -a app-name \t run using a different flask app"
        echo "  -e environ \t run using different flask environment (development or production)"
        echo "  -r host-name \t run using different flask hostname"
        echo "  -l size \t change how much data is needed before buffer flushing (>=1)"
        echo "  -h hours \t flush the buffer every so hours (>=0)"
        echo "  -m minutes \t flush the buffer every so minutes (>=0)"
        exit 0;;
  esac
done

#write back out parameters
FLASK_APP=$APP
FLASK_ENV=$ENV
FLASK_RUN_HOST=$HOST
FLUSH_LIMIT=$LIMIT
FLUSH_HOURS=$HOURS
FLUSH_MINUTES=$MINUTES

if $print; then
    echo " Running flask app '$FLASK_APP' in '$FLASK_ENV' environment with hostname '$FLASK_RUN_HOST'."
    echo " Flush size limit: $FLUSH_LIMIT"
    echo " Reflush every $FLUSH_HOURS hour(s) $FLUSH_MINUTES minute(s)"
    echo ""
fi

flask run
