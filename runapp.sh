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


#args=$(getopt -o "l:h:m:" -l "limit:,hours:,minutes:" -- "$@")
while getopts '?pl:h:m:' OPTION; do
  var=$(printf "%d\n" $OPTARG 2>/dev/null)
  case "$OPTION" in
    l)
        if [ $var -gt 0 ]; then
            export FLUSH_LIMIT=$OPTARG
        fi;;
    h)
        if [ $var -gt 0 ]||[ $var -eq 0 ]&&[ $FLUSH_MINUTES != 0 ]; then
            export FLUSH_HOURS=$OPTARG
        fi;;
    m)
        if [ $var -gt 0 ]||[ $var -eq 0 ]&&[ $FLUSH_HOURS != 0 ]; then
            export FLUSH_MINUTES=$OPTARG
        fi;;
    p)
        print=true;;
    ?)
        echo "usage: $0 [-?] [-p] [-l flush_size] [-h hrs_until_reflush] [-m min_until_reflush]"
        exit 0;;
  esac
done

if $print; then
    echo " Flush size limit: $FLUSH_LIMIT"
    echo " Reflush every $FLUSH_HOURS hour(s) $FLUSH_MINUTES minute(s)"
    echo ""
fi

flask run
