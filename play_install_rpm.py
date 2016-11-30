#!/usr/bin/env	python
#coding:utf-8

import ansible.playbook
from ansible import callbacks
from ansible import utils
from ansible.inventory import Inventory
import sys
import re
import json
import argparse
import getpass

class PasswordPromptAction(argparse.Action):
    def __init__(self,
             option_strings,
             dest=None,
             nargs=0,
             default=None,
             required=False,
             type=None,
             metavar=None,
             help=None):
        super(PasswordPromptAction, self).__init__(
             option_strings=option_strings,
             dest=dest,
             nargs=nargs,
             default=default,
             required=required,
             metavar=metavar,
             type=type,
             help=help)

    def __call__(self, parser, args, values, option_string=None):
        password = getpass.getpass()
        setattr(args, self.dest, password)

def installRpm(infoDic):
    playbookName = '/usr/local/repo/playbook/rpm.yml'
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats,verbose=utils.VERBOSITY)

    res = ansible.playbook.PlayBook(
    playbook = playbookName,
    stats = stats,
    callbacks = playbook_cb,
    runner_callbacks = runner_cb,
    inventory = Inventory(infoDic['hosts']),
    remote_user = infoDic['username'],
    remote_pass = infoDic['password'],
    extra_vars = infoDic, #add host list
    #only_tags = onlyTags,
    #skip_tags = ['mysql'],
    forks = 10
    )
    result=res.run()
    data=json.dumps(result)
    print data

def main(infoDic):
    installRpm(infoDic)

if __name__ == '__main__':
    if ( len( sys.argv ) == 1 ):
        print '\033[31m-h or --help for detail\033[0m'
        sys.exit(1)

    rpmdict = {'metaq':'metaq.zuche-1.0.0-1.el6.x86_64.rpm', 'memcache':'memcached.zuche-1.4.25-1.el6.x86_64.rpm', 'redis':'redis.zuche-2.8.24-1.el6.x86_64.rpm','zk':'zk.zuche-1.0.0-1.el6.x86_64.rpm','nginx':'nginx.zuche-1.5.2-1.el6.x86_64.rpm','tomcat':'tomcat.zuche-6.0.45-1.el6.x86_64.rpm' }

    parser = argparse.ArgumentParser()
    parser.add_argument('-r',required=True, help='rpmname example: \033[33mmetaq memcache redis zk nginx tomcat\033[0m')
    parser.add_argument('--host', required=True, help='host example: \037[32m10.1.1.1,10.1.1.2,10.1.1.3\033[0m')
    parser.add_argument('-u', required=True, help='username')
    parser.add_argument('-p', required=True,action=PasswordPromptAction, type=str, help='password')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    results = parser.parse_args()

    print results.host
    infoDic = {}
    infoDic['hosts'] = re.split(',| ',results.host)
    infoDic['rpmName'] = rpmdict[results.r]
    infoDic['username'] = results.u
    infoDic['password'] = results.p
    print 'rpmName : {0}'.format(infoDic['rpmName'])
    print 'hostList: {0}'.format(infoDic['hosts'])
    main(infoDic)
