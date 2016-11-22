#!/usr/local/bin/python
# encoding: utf-8
"""
*generate overview taskpaper documents containing tasks tagged with a sync-tags set within an entire workspace. There is also an option to sync with Apple Reminders (not implemented yet).*

:Author:
    David Young

:Date Created:
    November 15, 2016
"""
import sys
import os
import codecs
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from tastic.tastic import document
from fundamentals.files import recursive_directory_listing


class sync():
    """
    *The worker class for the sync module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``workspaceRoot`` -- path to the root folder of a workspace containing taskpaper files
        - ``workspaceName`` -- the name of the workspace
        - ``syncFolder`` -- path to a folder to host your synced tag taskpaper documents.

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a sync object, use the following:

        .. code-block:: python 

            from tastic.workspace import sync
            tp = sync(
                log=log,
                settings=settings,
                workspaceRoot="/path/to/workspace/root",
                workspaceName="myWorkspace",
                syncFolder="/path/to/sync/folder"
            )
            tp.sync()

        After this it is simply a matter of running `tp.sync()` to sync the sync-tag set into a taskpaper document in the syncFolder called `<workspaceName>-synced-tasks.taskpaper`
    """
    # INITIALISATION

    def __init__(
            self,
            log,
            workspaceRoot,
            workspaceName,
            syncFolder,
            settings=False
    ):
        self.log = log
        self.log.debug("instansiating a new 'sync' object")
        self.settings = settings
        self.workspaceRoot = workspaceRoot
        self.syncFolder = syncFolder
        self.workflowTags = self.settings["workflowTags"]
        syncTags = self.settings["syncTags"].replace("@", "").split(",")
        self.syncTags = []
        self.syncTags[:] = ["@" + s.strip() for s in syncTags]
        self.workspaceName = workspaceName

        # xt-self-arg-tmpx

        # INITIAL ACTIONS
        # RECURSIVELY CREATE MISSING DIRECTORIES - FOR SYNCED TASKPAPER DOCS
        if not os.path.exists(self.syncFolder):
            os.makedirs(self.syncFolder)

        return None

    def sync(self):
        """
        *sync the tasks tagged with a tag in the sync-tags set to index taskpaper document and HTML page*

        **Return:**
            - None

        see class docsting for usage

        """
        self.log.info('starting the ``sync`` method')

        taskpaperFiles = self._get_all_taskpaper_files(self.workspaceRoot)
        self._complete_original_tasks()

        content = self._get_tagged_content_from_taskpaper_files(taskpaperFiles)

        taskpaperDocPath = self._create_single_taskpaper_task_list(content)
        self._create_html_tasklist(taskpaperDocPath)

        # self._generate_sync_documents()

        self.log.info('completed the ``sync`` method')
        return None

    def _generate_sync_documents(
            self):
        """*generate sync documents*

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - update package tutorial if needed

            .. code-block:: python 

                usage code 

        """
        self.log.info('starting the ``_generate_sync_documents`` method')

        for tag in self.syncTags:
            pathToWriteFile = self.syncFolder + "/" + tag + ".taskpaper"
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToWriteFile,))
                writeFile = codecs.open(
                    pathToWriteFile, encoding='utf-8', mode='w')
            except IOError, e:
                message = 'could not open the file %s' % (pathToWriteFile,)
                self.log.critical(message)
                raise IOError(message)

            writeFile.close()

        self.log.info('completed the ``_generate_sync_documents`` method')
        return None

    def _get_all_taskpaper_files(
            self,
            workspaceRoot):
        """*get a list of all the taskpaper filepaths in the workspace (excluding the sync directory)*

        **Key Arguments:**
            - ``workspaceRoot`` -- path to the root folder of a workspace containing taskpaper files

        **Return:**
            - ``taskpaperFiles`` -- a list of paths to all the taskpaper files within the workspace
        """
        self.log.info('starting the ``_get_all_taskpaper_files`` method')

        theseFiles = recursive_directory_listing(
            log=self.log,
            baseFolderPath=self.workspaceRoot,
            whatToList="files"  # all | files | dirs
        )

        taskpaperFiles = []
        taskpaperFiles[:] = [f for f in theseFiles if os.path.splitext(f)[
            1] == ".taskpaper" and f != self.syncFolder]

        self.log.info('completed the ``_get_all_taskpaper_files`` method')
        return taskpaperFiles

    def _get_tagged_content_from_taskpaper_files(
            self,
            taskpaperFiles):
        """*get all tasks tagged with a sync-tag from taskpaper files*

        **Key Arguments:**
            - ``taskpaperFiles`` -- paths to all taskpaper files in workspace

        **Return:**
            - ``content`` -- the given tagged content of all taskpaper files in a workspace (string)
        """
        self.log.info(
            'starting the ``_get_tagged_content_from_taskpaper_files`` method')

        content = ""
        for tp in taskpaperFiles:
            # OPEN TASKPAPER FILE
            doc = document(tp)
            basename = os.path.basename(tp).replace("-", " ").upper()

            for tag in self.syncTags:
                filteredTasks = doc.tagged_tasks(tag)
                for ft in filteredTasks:
                    if "done" not in "".join(ft.tags):
                        if "Project" in ft.parent.__repr__():
                            thisNote = tp + " > " + ft.parent.title[:-1]
                        else:
                            thisNote = tp
                        ft.add_note(thisNote)
                        content += ft.to_string() + "\n"

        self.log.info(
            'completed the ``_get_tagged_content_from_taskpaper_files`` method')
        return content

    def _create_single_taskpaper_task_list(
            self,
            content):
        """*create single, sorted taskpaper task list from content pulled in from all of the workspace taskpaper docs*

        **Key Arguments:**
            - ``content`` -- the content to add to the taskpaper task index

        **Return:**
            - ``taskpaperDocPath`` -- path to the task index taskpaper doc
        """
        self.log.info(
            'starting the ``_create_single_taskpaper_task_list`` method')

        if len(content):
            content = content.decode("utf-8")
            taskpaperDocPath = self.syncFolder + "/" + \
                self.workspaceName + "-synced-tasks.taskpaper"
            try:
                self.log.debug("attempting to open the file %s" %
                               (taskpaperDocPath,))
                writeFile = codecs.open(
                    taskpaperDocPath, encoding='utf-8', mode='w')
            except IOError, e:
                message = 'could not open the file %s' % (taskpaperDocPath,)
                self.log.critical(message)
                raise IOError(message)
            writeFile.write(content)
            writeFile.close()
            # OPEN TASKPAPER FILE
            doc = document(self.syncFolder + "/" +
                           self.workspaceName + "-synced-tasks.taskpaper")
            doc.sort_projects(workflowTags=self.workflowTags)
            doc.sort_tasks(workflowTags=self.workflowTags)
            doc.save()

        self.log.info(
            'completed the ``_create_single_taskpaper_task_list`` method')
        return taskpaperDocPath

    def _create_html_tasklist(
            self,
            taskpaperDocPath):
        """*create an html version of the single taskpaper index task list*

        **Key Arguments:**
            - ``taskpaperDocPath`` -- path to the task index taskpaper doc

        **Return:**
            - ``htmlFilePath`` -- the path to the output HTML file
        """
        self.log.info('starting the ``_create_html_tasklist`` method')

        title = self.workspaceName
        content = "<h1>%(title)s tasks</h1><ul>\n" % locals()

        # OPEN TASKPAPER FILE
        doc = document(taskpaperDocPath)
        docTasks = doc.tasks

        for task in docTasks:

            tagString = " ".join(task.tags)
            tagString2 = ""
            for t in task.tags:
                tagString2 += """ <span class="%(t)s tag">@%(t)s</span>""" % locals()

            notes = task.notes
            filepath = notes[0].title.split(" > ")[0]
            basename = os.path.basename(filepath).replace(
                ".taskpaper", "").replace("-", " ")
            filepath = "dryx-open://" + filepath
            taskTitle = u"""<a href="%(filepath)s"><span class="bullet %(tagString)s">◉</span> </a>""" % locals() + \
                task.title[2:] + tagString2

            if len(notes[0].title.split(" > ")) > 1:
                parent = notes[0].title.split(" > ")[1]
                parent = """<span class="parent">%(basename)s > %(parent)s</span></br>\n""" % locals(
                )
            else:
                parent = """<span class="parent">%(basename)s</span></br>\n""" % locals(
                )
            taskContent = """</span>\n\t\t</br><span class="notes">""".join(task.to_string(
                title=False, indentLevel=0).split("\n")[1:])
            if len(taskContent):
                taskContent = """\n\t<br><span class="notes">""" + \
                    taskContent + """\n\t</span>"""
            else:
                taskContent = ""

            htmlTask = """<li class="XXX">%(parent)s%(taskTitle)s%(taskContent)s</li>\n"""  % locals()
            content += htmlTask

        content += "</ul>"

        htmlFilePath = taskpaperDocPath.replace(".taskpaper", ".html")
        try:
            self.log.debug("attempting to open the file %s" % (htmlFilePath,))
            writeFile = codecs.open(
                htmlFilePath, encoding='utf-8', mode='w')
        except IOError, e:
            message = 'could not open the file %s' % (htmlFilePath,)
            self.log.critical(message)
            raise IOError(message)
        writeFile.write(content)
        writeFile.close()

        self.log.info('completed the ``_create_html_tasklist`` method')
        return htmlFilePath

    def _complete_original_tasks(
            self):
        """*mark original tasks as completed if they are marked as complete in the index taskpaper document*
        """
        self.log.info('starting the ``_complete_original_tasks`` method')

        taskpaperDocPath = self.syncFolder + "/" + \
            self.workspaceName + "-synced-tasks.taskpaper"
        exists = os.path.exists(taskpaperDocPath)
        if not exists:
            return

        # OPEN TASKPAPER INDEX FILE
        doc = document(taskpaperDocPath)
        doneTasks = doc.tagged_tasks("@done")

        for t in doneTasks:
            theseNotes = t.notes
            parent = t.parent
            while not len(theseNotes) and parent and parent.parent:
                theseNotes = parent.notes
                parent = parent.parent

            originalFile = theseNotes[0].title.split(" > ")[0].strip()
            if len(theseNotes[0].title.split(" > ")) > 1:
                projectName = theseNotes[0].title.split(" > ")[1].strip()
            else:
                projectName = False

            odoc = document(originalFile)
            odoc.tidy()
            odoc.save()
            odoc = document(originalFile)
            if projectName:
                thisObject = odoc.get_project(projectName)
            else:
                thisObject = odoc

            oTask = thisObject.get_task(t.title)
            if oTask:
                oTask.done("all")
                odoc.save()

        self.log.info('completed the ``_complete_original_tasks`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
