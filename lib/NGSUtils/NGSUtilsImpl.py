# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import os
import subprocess
import uuid

from pprint import pformat

from ReadsUtils.ReadsUtilsClient import ReadsUtils
from KBaseReport.KBaseReportClient import KBaseReport
#END_HEADER


class NGSUtils:
    '''
    Module Name:
    NGSUtils

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "1.0.0"
    GIT_URL = "git@github.com:kbaseapps/ngsutils"
    GIT_COMMIT_HASH = "8caeed3610b06f829ac93dc2bab61c01b2c84a67"

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    workspaceURL = None
    FASTQUTILS = 'fastqutils'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.workspaceURL = config['workspace-url']
        self.scratch = os.path.abspath(config['scratch'])
        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
        #END_CONSTRUCTOR
        pass


    def fastqutils_stats(self, ctx, params):
        """
        :param params: instance of type "FastqUtilsStatsParams" -> structure:
           parameter "workspace_name" of type "workspace_name" (A string
           representing a workspace name.), parameter "read_library_ref" of
           type "read_library_ref" (A string representing a ContigSet id.)
        :returns: instance of type "FastqUtilsStatsResult" -> structure:
           parameter "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fastqutils_stats

        print('Running fastqutils_stats with params=')
        print(pformat(params))

        if 'workspace_name' not in params:
            raise ValueError('workspace_name parameter is required')
        if 'read_library_ref' not in params:
            raise ValueError('read_library_ref parameter is required')

        # Get the read library as deinterleaved fastq files
        input_ref = params['read_library_ref']
        reads_params = {'read_libraries': [input_ref],
                        'interleaved': 'false',
                        'gzipped': None
                        }
        ru = ReadsUtils(self.callbackURL, token=ctx['token'])
        reads = ru.download_reads(reads_params)['files']
        files = [reads[input_ref]['files']['fwd']]
        if reads[input_ref]['files']['rev']:
            files.append(reads[input_ref]['files']['rev'])
        print('running on files:')
        for f in files:
            print(f)

        # construct the command
        stats_cmd = [self.FASTQUTILS, 'stats']

        report = ''
        for f in files:
            cmd = stats_cmd
            cmd.append(f)

            report += '============== ' + f + ' ==============\n'
            print('running: ' + ' '.join(cmd))
            p = subprocess.Popen(cmd,
                                 cwd=self.scratch,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 shell=False)

            while True:
                line = p.stdout.readline()
                if not line:
                    break
                report += line
                print(line.replace('\n', ''))

            p.stdout.close()
            p.wait()
            report += "\n\n"
            print('return code: ' + str(p.returncode))
            if p.returncode != 0:
                raise ValueError('Error running ' + self.FASTQUTILS + ', return code: ' + str(p.returncode))


        reportObj = {
            'objects_created': [],
            'text_message': report
        }
        report = KBaseReport(self.callbackURL)
        report_info = report.create({'report': reportObj, 'workspace_name': params['workspace_name']})
        returnVal = {'report_name': report_info['name'], 'report_ref': report_info['ref']}

        #END fastqutils_stats

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fastqutils_stats return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
