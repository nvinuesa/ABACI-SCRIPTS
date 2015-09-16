#!/bin/bash
#
# Script that moves DICOM/PDF/CSV data from the harddrive into XNat
# (Hauke Bartsch, hbartsch@ucsd.edu)
# requires: dcmtk, curl
# add your user name, password and server name
#

if [ $# -ne 7 ]
then
  echo "Usage: provide <project id>, <subject id>, <visit id>, <data directory>, <user>, <password> and <xnat_site>"
  echo "       Data in the directory is scanned for DICOM data, all other files are uploaded as binary."
  exit;
fi
echo "done"

subject=$2
session=$3
directory=$4
USER=$5
PASSWORD=$6
PROJECT=$1
XNAT=$7

dir=`pwd`
if [ ! -d $directory ]; then
  echo "Error: subject directory ($directory) does not exist"
  exit;
fi

# Create a session cookie, we want to re-use that session instead of providing
# login information every time. Number of sessions might be limited otherwise to 1000.
cookie=`curl -k -u $USER:$PASSWORD -X POST $XNAT/data/JSESSION`
echo "Session ID is: $cookie"

# create subject in case it does not exist
echo "create subject $c"
c=`curl --cookie JSESSIONID=$cookie -k -X PUT $XNAT/data/archive/projects/$PROJECT/subjects/$subject`
# create session in case it does not exist
echo "create session $c"
c=`curl --cookie JSESSIONID=$cookie -k -X PUT $XNAT/data/archive/projects/$PROJECT/subjects/$subject/experiments/$session?xsiType=xnat:mrSessionData`

timestamps=( )
for file in `find $directory -type f -print`
do 

     # move file over using REST API
     c=`curl  --cookie JSESSIONID=$cookie -s -k -H 'Content-Type: application/dicom' -X POST "$XNAT/data/services/import?inbody=true&PROJECT_ID=$PROJECT&SUBJECT_ID=$subject&EXPT_LABEL=$session&prearchive=true&overwrite=append&format=DICOM&content=T1_RAW" --data-binary @$file | tr -d [:cntrl:]`
     echo -n "."
     timestamp=`echo $c | cut -d'/' -f6`
     # is timestamp new?
     found="0"
     for f in "${timestamps[@]}"; do
        if [ "$f" = "$timestamp" ]; then

           found="1"
        fi
     done
     # add to array
     if [ $found = "0" ]; then
        timestamps+=($timestamp)
        echo "found a new series $timestamp"
     fi

done
echo "done sending files..."
