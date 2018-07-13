#!/usr/bin/env python
# coding=utf-8

"""
Created on  2018-07-10 16:26:48
Author:     Bai
"""

import sys
import json
import subprocess as sp
from os import path
from collections import Counter

from docopt import docopt

doc = """
Usage:
  ./{} [--debug] [PATH]

Arguments:
  PATH    Scan files in the given path (the current directory by default).

Options:
  -h --help              show this help message and exit
  -v --version           show version and exit
  --debug                show all arguments
""".format(sys.argv[0])


def cmd_line(params):
    if params['--debug']:
        print(params)
        sys.exit(1)

    if params['PATH']:
        cmd = 'ncdu -o- {}'.format(params['PATH'])
    else:
        cmd = 'ncdu -o-'

    return cmd


def run(cmd):
    rt = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdout, stderr) = rt.communicate()
    rc = rt.returncode
    if rc != 0:
        print 'command execute failed: ', cmd
        print '==== error ====\n', stderr
        sys.exit(rc)
    return stdout


def load_data(data):
    pdata = json.loads(data, encoding='latin1')[-1]
    # print json.dumps(pdata, indent=4)
    return analyze_data(pdata)


def analyze_data(data, updir=None, bigdirs=None, bigfiles=None):
    if bigdirs is None:
        bigdirs = {}
    if bigfiles is None:
        bigfiles = {}
    if updir is None:
        dirpath = data[0]['name']
    else:
        dirpath = path.join(updir, data[0]['name'])

    bigdirs[dirpath] = data[0].get('asize', 0)

    for i in data[1:]:
        if type(i) == dict:
            if 'dsize' not in i or 'asize' not in i or 'notreg' in i:
                filesize = 0
            else:
                # try:
                filesize = i['dsize']
                # except KeyError:
                #    print 'this is error, dirpath: ',dirpath,'and file:',i
                #    sys.exit(1)
            bigdirs[dirpath] += filesize
            filepath = path.join(dirpath, i['name'])
            bigfiles[filepath] = filesize
        else:
            analyze_data(i, dirpath, bigdirs, bigfiles)
    return bigdirs, bigfiles


def main():
    args = docopt(doc, version='2018.07.13')
    ncdudata = run(cmd_line(args))
    bigdirs, bigfiles = load_data(ncdudata)
    topdirs = Counter(bigdirs).most_common()[0:9]
    topfiles = Counter(bigfiles).most_common()[0:9]
    print topdirs, topfiles


if __name__ == '__main__':
    main()
