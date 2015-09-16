#!/bin/bash

# Copyright (C) 2015 nicolasvinuesa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script uses most of Hauke Bartsch's own dicom uploader for XNAT 
# it iterates over a directorye and runs his code.

if [ $# -lt 5 ]
  then
	echo 'usage: importDcm.sh <site> <user> <password> <project> <directory>'
	echo '<site>        : Site to be used (e.g.: http://localhost:8080/xnat).'
	echo '<user>        : Site username (e.g.: admin).'
	echo '<password>    : Site password (e.g.: admin).'  
	echo '<project>     : Project to import images on.' 
	echo '<directory>   : Directory where raw images are on.' 
	exit 1
fi

SITE=$1
USER=$2
PASSWORD=$3
PROJECT=$4
directory=$5


totalNumberSubjects=`find $directory -maxdepth 1 -mindepth 1 -type d | wc -l`
currentSubject=1
for subj in `find $directory -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort -V` 
do 
     echo "Subject $subj ($currentSubject/$totalNumberSubjects)"
     totalNumberSessions=`find $directory/$subj -maxdepth 1 -mindepth 1 -type d | wc -l`
     currentSession=1
     for sess in `find $directory/$subj -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort -V`
     do
	echo "Uploading session $sess ($currentSession/$totalNumberSessions) of subject $subj."
     	./import2xnat.sh $PROJECT $subj $sess $directory/$subj/$sess $USER $PASSWORD $SITE
	currentSession=$(($currentSession+1))
	echo ""
     done   
     currentSubject=$(($currentSubject+1))
     echo ""
done


