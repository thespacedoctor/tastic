#!/usr/local/bin/python
# encoding: utf-8
"""
*sorts the contents of all taskpaper files via workflow tags*

:Author:
    David Young

:Date Created:
    November  5, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from fundamentals.renderer import list_of_dictionaries
from operator import itemgetter
import collections
import codecs
import textwrap
from tastic.tastic import document


class workspace():
    """
    *tools for sorting, archiving and indexing tasks and maintaining the contents of all taskpaper files within a given workspace*

    **Key Arguments:**
        - ``log`` -- logger
        - ``fileOrWorkspacePath`` -- the root path of the workspace you wish to sort the taskpaper docs within, or the path to a single taskpaper file
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a taskpaper workspace object, use the following:

        .. code-block:: python 

            from tastic.workspace import workspace
            ws = workspace(
                log=log,
                settings=settings,
                fileOrWorkspacePath="/path/to/root/of/workspace"
            )

        or to target a single taskpaper document use instead the path to the file:

        .. code-block:: python 

            from tastic.workspace import workspace
            ws = workspace(
                log=log,
                settings=settings,
                fileOrWorkspacePath="/path/to/doc.taskpaper"
            )
    """
    # Initialisation

    def __init__(
            self,
            log,
            fileOrWorkspacePath,
            settings=False
    ):
        self.log = log
        log.debug("instansiating a new 'sort' object")
        self.settings = settings
        self.taskpaperPath = False
        self.workspaceRoot = False
        # xt-self-arg-tmpx

        # INITIAL ACTIONS
        # ARE WE DEALING WITH A WORKSPACE DIRECTORY OR SINGLE FILE
        if os.path.isfile(fileOrWorkspacePath):
            self.taskpaperPath = fileOrWorkspacePath
        else:
            self.workspaceRoot = fileOrWorkspacePath

        self.taskpaperFiles = self._get_all_taskpaper_files()

        return None

    def sort(self):
        """
        *sort the workspace or individual taskpaper document via the workflow tags found in the settings file*

        **Usage:**

            To sort all of the taskpaper documents in the workspace via the workflow tag set with the settings file, for example:

            .. code-block:: yaml

                workflowTags: "@due, @flag, @hold, @next, @someday, @wait" 

            use the ``sort()`` method:

            .. code-block:: python 

                ws.sort()
        """
        self.log.info('starting the ``sort`` method')

        for f in self.taskpaperFiles:
            self._sort_tp_file(f)

        self.log.info('completed the ``sort`` method')
        return None

    def archive_done(
            self):
        """*move done tasks from the document's 'Archive' project into an adjacent markdown tasklog file*

        **Usage:**

            To move the archived tasks within a workspace's taskpaper docs into ``-tasklog.md`` files use the ``archive_done()`` method:

            .. code-block:: python 

                ws.archive_done()
        """
        self.log.info('starting the ``archive_done`` method')

        for f in self.taskpaperFiles:
            self._archive_tp_file_done_tasks(f)

        self.log.info('completed the ``archive_done`` method')
        return None

    def _get_all_taskpaper_files(
            self):
        """*get a list of all the taskpaper filepaths in the workspace*

        **Return:**
            - ``taskpaperFiles`` -- a list of paths to all the taskpaper files within the workspace
        """
        self.log.info('starting the ``_get_all_taskpaper_files`` method')

        if self.workspaceRoot:
            from fundamentals.files import recursive_directory_listing
            theseFiles = recursive_directory_listing(
                log=self.log,
                baseFolderPath=self.workspaceRoot,
                whatToList="files"  # all | files | dirs
            )

            taskpaperFiles = []
            taskpaperFiles[:] = [f for f in theseFiles if os.path.splitext(f)[
                1] == ".taskpaper"]
        else:
            taskpaperFiles = [self.taskpaperPath]

        self.log.info('completed the ``_get_all_taskpaper_files`` method')
        return taskpaperFiles

    def _sort_tp_file(
            self,
            taskpaperPath):
        """*sort individual taskpaper documents*

        **Key Arguments:**
            - ``taskpaperPath`` -- path to a taskpaper file

        **Return:**
            - None
        """
        self.log.info('starting the ``_sort_tp_file`` method')

        # OPEN TASKPAPER FILE

        self.log.info("sorting taskpaper file %(taskpaperPath)s" % locals())
        doc = document(taskpaperPath)
        doc.tidy()
        doc.sort_tasks(self.settings["workflowTags"])
        doc.sort_projects(self.settings["workflowTags"])
        doc.save()

        self.log.info('completed the ``_sort_tp_file`` method')
        return None

    def _archive_tp_file_done_tasks(
            self,
            taskpaperPath):
        """* archive tp file done tasks*

        **Key Arguments:**
            - ``taskpaperPath`` -- path to a taskpaper file

        **Return:**
            - None
        """
        self.log.info('starting the ``_archive_tp_file_done_tasks`` method')
        self.log.info("archiving taskpaper file %(taskpaperPath)s" % locals())
        taskLog = {}
        mdArchiveFile = taskpaperPath.replace(".taskpaper", "-tasklog.md")
        exists = os.path.exists(mdArchiveFile)
        if exists:
            pathToReadFile = mdArchiveFile
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(
                    pathToReadFile, encoding='utf-8', mode='r')
                thisData = readFile.read()
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()
            table = False
            for l in thisData.split("\n"):
                l = l.encode("utf-8")
                if ":---" in l:
                    table = True
                    continue
                if table == True and len(l) and l[0] == "|":
                    dictt = collections.OrderedDict(sorted({}.items()))
                    columns = l.split("|")

                    dictt["task"] = columns[1].strip()
                    dictt["completed"] = columns[2].strip()
                    dictt["project"] = columns[3].strip()
                    taskLog[dictt["task"] + dictt["completed"] +
                            dictt["project"]] = dictt

        doc = document(taskpaperPath)
        aProject = doc.get_project("Archive")
        if not aProject:
            return

        doneTasks = aProject.tagged_tasks("@done")

        for task in doneTasks:
            dateCompleted = ""
            project = ""
            for t in task.tags:
                if "done" in t:
                    dateCompleted = t.replace("done", "").replace(
                        "(", "").replace(")", "")
                if "project(" in t:
                    project = t.replace("project", "").replace(
                        "(", "").replace(")", "")

            dictt = collections.OrderedDict(sorted({}.items()))

            notes = ""
            if task.notes:
                for n in task.notes:
                    if len(notes) and notes[-2:] != ". ":
                        if notes[-1] == ".":
                            notes += " "
                        else:
                            notes += ". "
                    notes += n.title
            if len(notes):
                notes = "<br><br>**NOTES:**<br>" + \
                    "<br>".join(textwrap.wrap(
                        notes, 120, break_long_words=True))

            dictt["task"] = "<br>".join(textwrap.wrap(task.title[
                2:], 120, break_long_words=True)) + notes
            dictt["task"] = dictt["task"].encode("utf-8")
            dictt["completed"] = dateCompleted
            dictt["project"] = project

            # SET ENCODE ERROR RETURN VALUE

            # RECODE INTO ASCII
            dictt["task"] = dictt["task"].decode("utf-8")
            taskLog[dictt["task"] + dictt["completed"] +
                    dictt["project"]] = dictt

        taskLog = taskLog.values()

        taskLog = sorted(taskLog, key=itemgetter('task'), reverse=True)
        taskLog = sorted(taskLog, key=itemgetter('project'), reverse=True)
        taskLog = sorted(taskLog, key=itemgetter('completed'), reverse=True)

        dataSet = list_of_dictionaries(
            log=self.log,
            listOfDictionaries=taskLog
        )

        markdownData = dataSet.markdown(filepath=None)

        try:
            self.log.debug("attempting to open the file %s" % (mdArchiveFile,))
            writeFile = codecs.open(mdArchiveFile, encoding='utf-8', mode='w')
        except IOError, e:
            message = 'could not open the file %s' % (mdArchiveFile,)
            self.log.critical(message)
            raise IOError(message)

        writeFile.write(markdownData.decode("utf-8"))
        writeFile.close()

        aProject.delete()

        doc.save()

        self.log.info('completed the ``_archive_tp_file_done_tasks`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
