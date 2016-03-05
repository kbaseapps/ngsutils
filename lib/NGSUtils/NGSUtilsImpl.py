#BEGIN_HEADER
# The header block is where all import statments should live
import os
import sys
import shutil
import hashlib
import subprocess
import requests
import re
import traceback
import uuid
from datetime import datetime
from pprint import pprint, pformat

import numpy as np

from Bio import SeqIO

from biokbase.workspace.client import Workspace as workspaceService

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
#END_HEADER


class NGSUtils:
    '''
    Module Name:
    NGSUtils

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    workspaceURL = None
    FASTQUTILS = 'fastqutils'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.scratch = os.path.abspath(config['scratch'])
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
        #END_CONSTRUCTOR
        pass

    def fastqutils_stats(self, ctx, params):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fastqutils_stats

        print('Running fastqutils_stats with params=')
        print(pformat(params))

        #### do some basic checks
        objref = ''
        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'read_library_name' not in params:
            raise ValueError('read_library_name parameter is required')

        #### Get the read library
        try:
            ws = workspaceService(self.workspaceURL, token=ctx['token'])
            objects = ws.get_objects([{'ref': params['workspace_name']+'/'+params['read_library_name']}])
            data = objects[0]['data']
            info = objects[0]['info']
            # Object Info Contents
            # absolute ref = info[6] + '/' + info[0] + '/' + info[4]
            # 0 - obj_id objid
            # 1 - obj_name name
            # 2 - type_string type
            # 3 - timestamp save_date
            # 4 - int version
            # 5 - username saved_by
            # 6 - ws_id wsid
            # 7 - ws_name workspace
            # 8 - string chsum
            # 9 - int size 
            # 10 - usermeta meta
            type_name = info[2].split('.')[1].split('-')[0]
        except Exception as e:
            raise ValueError('Unable to fetch read library object from workspace: ' + str(e))
            #to get the full stack trace: traceback.format_exc()


        files = []

        #### Download the paired end library
        if type_name == 'PairedEndLibrary':
            try:
                fr_type = ''
                rv_type = ''
                if 'lib1' in data:
                    forward_reads = data['lib1']['file']
                    # type is required if lib1 is present
                    fr_type = '.' + data['lib1']['type']
                elif 'handle_1' in data:
                    forward_reads = data['handle_1']
                if 'lib2' in data:
                    reverse_reads = data['lib2']['file']
                    # type is required if lib2 is present
                    rv_type = '.' + data['lib2']['type']
                elif 'handle_2' in data:
                    reverse_reads = data['handle_2']
                else:
                    reverse_reads={}

                fr_file_name = forward_reads['id'] + fr_type
                if 'file_name' in forward_reads:
                    fr_file_name = forward_reads['file_name']
                
                ### NOTE: this section is what could be replaced by the transform services
                forward_reads_file_location = os.path.join(self.scratch,fr_file_name)
                forward_reads_file = open(forward_reads_file_location, 'w', 0)
                print('downloading reads file: '+str(forward_reads_file_location))
                headers = {'Authorization': 'OAuth '+ctx['token']}
                r = requests.get(forward_reads['url']+'/node/'+forward_reads['id']+'?download', stream=True, headers=headers)
                for chunk in r.iter_content(1024):
                    forward_reads_file.write(chunk)
                forward_reads_file.close();
                print('done')
                files = [fr_file_name]
                ### END NOTE

                if 'interleaved' in data and data['interleaved']:
                    # we don't do any processing on interleaved files
                    pass
                else:
                    # we need to read in reverse reads file separately
                    rev_file_name = reverse_reads['id'] + rv_type
                    if 'file_name' in reverse_reads:
                        rev_file_name = reverse_reads['file_name']
                    ### NOTE: this section is what could also be replaced by the transform services
                    reverse_reads_file_location = os.path.join(self.scratch,rev_file_name)
                    reverse_reads_file = open(reverse_reads_file_location, 'w', 0)
                    print('downloading reverse reads file: '+str(reverse_reads_file_location))
                    r = requests.get(reverse_reads['url']+'/node/'+reverse_reads['id']+'?download', stream=True, headers=headers)
                    for chunk in r.iter_content(1024):
                        reverse_reads_file.write(chunk)
                    reverse_reads_file.close()
                    print('done')
                    files = [fr_file_name, rev_file_name]
                    ### END NOTE
            except Exception as e:
                print(traceback.format_exc())
                raise ValueError('Unable to download paired-end read library files: ' + str(e))
        elif type_name == 'SingleEndLibrary':
            try:
                if 'lib' in data:
                    forward_reads = data['lib']['file']
                elif 'handle' in data:
                    forward_reads = data['handle']

                fr_file_name = forward_reads['id']
                if 'file_name' in forward_reads:
                    fr_file_name = forward_reads['file_name']
                
                ### NOTE: this section is what could be replaced by the transform services
                forward_reads_file_location = os.path.join(self.scratch,fr_file_name)
                forward_reads_file = open(forward_reads_file_location, 'w', 0)
                print('downloading reads file: '+str(forward_reads_file_location))
                headers = {'Authorization': 'OAuth '+ctx['token']}
                r = requests.get(forward_reads['url']+'/node/'+forward_reads['id']+'?download', stream=True, headers=headers)
                for chunk in r.iter_content(1024):
                    forward_reads_file.write(chunk)
                forward_reads_file.close();
                print('done')
                files = [fr_file_name]
                ### END NOTE

            except Exception as e:
                print(traceback.format_exc())
                raise ValueError('Unable to download paired-end read library files: ' + str(e)) 
        else:
            raise ValueError('Cannot yet handle library type of: '+type_name)

        # construct the command
        stats_cmd = [self.FASTQUTILS, 'stats']

        report = ''
        for f in files:
            cmd = stats_cmd
            cmd.append(f)

            report += '============== '+ f + ' ==============\n'
            print('running: '+' '.join(cmd))
            p = subprocess.Popen(cmd,
                        cwd = self.scratch,
                        stdout = subprocess.PIPE, 
                        stderr = subprocess.STDOUT, shell = False)

            while True:
                line = p.stdout.readline()
                if not line: break
                report += line
                print(line.replace('\n', ''))

            p.stdout.close()
            p.wait()
            report += "\n\n"
            print('return code: ' + str(p.returncode))
            if p.returncode != 0:
                raise ValueError('Error running '+self.FASTQUTILS+', return code: '+str(p.returncode))


        reportObj = {
            'objects_created':[],
            'text_message':report
        }

        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']

        reportName = 'ngsutils_stats_report_'+str(hex(uuid.getnode()))
        report_obj_info = ws.save_objects({
                'id':info[6],
                'objects':[
                    {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1,
                        'provenance':provenance
                    }
                ]
            })[0]

        returnVal = { 'report_name': reportName, 'report_ref': str(report_obj_info[6]) + '/' + str(report_obj_info[0]) + '/' + str(report_obj_info[4]) }
        #END fastqutils_stats

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fastqutils_stats return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
