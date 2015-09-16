#!/usr/bin/python

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

__author__="nicolasvinuesa"
__date__ ="$Jul 31, 2015 10:52:12 AM$"

import sys
import getopt
import json
import urllib2
import base64
import getpass

def launch(site, user, password, project, pipeline, args):
    request = urllib2.Request(site + "/data/archive/projects/" + project + "/experiments?format=json")
    base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    response = urllib2.urlopen(request)
    html = response.read()
    data = json.loads(html)
    experiments = data['ResultSet']['Result']
    for exp in experiments:
        print('Launching ' + pipeline + ' on experiment ' +exp['ID'])
        request = urllib2.Request(site + "/REST/projects/" + project + "/pipelines/" + pipeline + "/experiments/" + exp['ID'] + "?" + args)
        request.add_header("Authorization", "Basic %s" % base64string) 
        response = urllib2.urlopen(request, '')
        html = response.read()
        
def main():
    # Get input arguments and define usage:
    o, a = getopt.getopt(sys.argv[1:], "hs:u:p:j:i:a:")
    if len(o) == 0:
	print('ABACI pipeline launcher')
	print('  Launchs a pipeline over all the subjects in one project. Be carefull since the input arguments (e.g. scan number of the T1 sequence) must be the same for ALL subjects in the project.')
	print('')
        site = "http://localhost:8080/xnat"        
        print('The site you are using is: ' + site)
        user = raw_input('Please enter your username: ')
        password = getpass.getpass()
        # Obtain a list of projects present at the site:
        request = urllib2.Request(site + "/REST/projects?format=json")
        base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        response = urllib2.urlopen(request)
        html = response.read()
        data = json.loads(html)
        projectsIt = data['ResultSet']['Result']
        # Print the list of projects:    
        st = ''
        for pr in projectsIt:
            st = st + pr['ID'] + ','
        print('Available projects in the site: ' + st)                
        project = raw_input('Please select a project: ')
        # Obtain a list of pipelines present at the chosen project:
        request = urllib2.Request(site + "/data/projects/" + project + "/pipelines?format=json")
        base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        response = urllib2.urlopen(request)
        html = response.read()
        data = json.loads(html)
        pipeIt = data['ResultSet']['Result']
        # Print the list of projects:    
        st = ''
        for pi in pipeIt:
            st = st + pi['Name'] + ','
        print('Available pipelines in the project: ' + st)                
        pipeline = raw_input('Please select a pipeline: ')
        # Obtain the list of input parameters on the chosen pipeline:
        request = urllib2.Request(site + "/data/projects/" + project + "/pipelines/" + pipeline)
        base64string = base64.encodestring('%s:%s' % (user, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        response = urllib2.urlopen(request)
        html = response.read()
        data = json.loads(html)
	argIt = data['inputParameters']
        # Get user input for each one of the parameters:    
        print('Set the input parameters for the pipeline (leave blank to use DEFAULT VALUES):')
	args = ''
        for i in range(0,len(data['inputParameters'])):
	    arg = raw_input('  ' + data['inputParameters'][i]['name'] + ': ')
	    if arg:
		#args = args + data['inputParameters'][i]['values'][data['inputParameters'][i]['values'].keys()[0]] + '=' + arg + ';' 
            	args = args + data['inputParameters'][i]['name'] + '=' + arg + '&'
        args = args[:-1]
	print('###')
	conf = ''
	while (conf != 'y' and conf != 'N'):
	    conf = raw_input('Confirm launch [y/N]: ')
	    if (conf == 'y'):
		launch(site, user, password, project, pipeline, args)
	    elif (conf == 'N'):
		sys.exit()
            
    else:   
	if (len(o) == 1 or len(o) == 6):   
            for opt, arg in o:
                if opt == '-h':
                    print 'usage: pipelineprojectlauncher.py [-h] -s <site> -u <user> -p <password> -j <project> -i <pipeline> -a <pipeline_arguments>'
                    print '-s <site>        		: Site to be used (e.g.: http://localhost:8080/xnat).'
                    print '-u <user>            	: Site username (e.g.: admin).'
                    print '-p <password>    	   	: Site password (e.g.: admin).'  
                    print '-j <project>  		: Project to launch pipeline on.' 
                    print '-i <pipeline> 		: Pipeline to be launch on the selected project.' 
                    print '-a <pipeline_arguments> 	: Pipeline input arguments, separated by & (e.g.: scanids=3,4,5&template=toto.nii). Input arguments which are not set by you will use their default values.' 
                    sys.exit()
                elif opt == '-s':
                    site = arg
                elif opt == '-u':
                    user = arg
                elif opt == '-p':
                    password = arg
                elif opt == '-j':
                    project = arg    
                elif opt == '-i':
                    pipeline = arg 
                elif opt == '-a':
                    args = arg 
		
	    launch(site, user, password, project, pipeline, args)

	else:
	    print 'Wrong number of arguments!'
	    print 'usage: pipelineprojectlauncher.py [-h] -s <site> -u <user> -p <password> -j <project> -i <pipeline> -a <pipeline_arguments>'
            print '-s <site>        		: Site to be used (e.g.: http://localhost:8080/xnat).'
            print '-u <user>            	: Site username (e.g.: admin).'
            print '-p <password>    	   	: Site password (e.g.: admin).'  
            print '-j <project>  		: Project to launch pipeline on.' 
            print '-i <pipeline> 		: Pipeline to be launch on the selected project.' 
            print '-a <pipeline_arguments> 	: Pipeline input arguments, separated by & (e.g.: scanids=3,4,5&template=toto.nii). Input arguments which are not set by you will use their default values.' 
	    sys.exit(2)

if __name__ == "__main__":
    main()
