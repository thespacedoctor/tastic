#!/usr/local/bin/python
# encoding: utf-8
"""
Documentation for tastic can be found here: http://tastic-for-taskpaper.readthedocs.io/en/stable/


Usage:
    tastic init
    tastic sort <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
    tastic archive <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
    tastic sync <pathToWorkspace> <workspaceName> <pathToSyncFolder> [-s <pathToSettingsFile>]
    tastic reminders import <listName> <pathToTaskpaperDoc>

Options:
    init                     setup the tastic settings file for the first time
    sort                     sort a taskpaper file or directory containing taskpaper files via workflow tags in settings file
    archive                  move done tasks in the 'Archive' projects within taskpaper documents into markdown tasklog files
    reminders                commands to work with macOS reminders
    import                   import tasks into a given taskpaper document


    pathToFileOrWorkspace    give a path to an individual taskpaper file or the root of a workspace containing taskpaper files
    pathToTaskpaperDoc       a path to a taskpaper document
    pathToWorkspace          root path of a workspace containing taskpaper files
    workspaceName            the name you give to the workspace
    pathToSyncFolder         path to the folder you wish to sync the index task files into
    listName                 name of a reminders.app list (macOS only)
    -h, --help               show this help message
    -v, --version            show version
    -s, --settings           the settings file

"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT
from . import workspace
from . import sync as syncc
from . import reminders as reminderss
# from ..__init__ import *


def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="DEBUG",
        options_first=False,
        projectName="tastic"
    )
    arguments, settings, log, dbConn = su.setup()

    # unpack remaining cl arguments using `exec` to setup the variable names
    # automatically
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if varname == "import":
            varname = "iimport"
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    if init:
        from os.path import expanduser
        home = expanduser("~")
        filepath = home + "/.config/tastic/tastic.yaml"
        try:
            cmd = """open %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        try:
            cmd = """start %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass

    # CALL FUNCTIONS/OBJECTS
    if sort or archive:

        ws = workspace(
            log=log,
            settings=settings,
            fileOrWorkspacePath=pathToFileOrWorkspace
        )
    if sort:
        ws.sort()
    if archive:
        ws.archive_done()

    if sync:
        tp = syncc(
            log=log,
            settings=settings,
            workspaceRoot=pathToWorkspace,
            workspaceName=workspaceName,
            syncFolder=pathToSyncFolder
        )
        tp.sync()

    if reminders:
        r = reminderss(
            log=log,
            settings=settings
        )
        r.import_list(
            listName=listName,
            pathToTaskpaperDoc=pathToTaskpaperDoc
        )

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


if __name__ == '__main__':
    main()
