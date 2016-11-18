#!/usr/local/bin/python
# encoding: utf-8
"""
*generate overview taskpaper documents containing all projects and tasks tagged with a workflow tag within an entire workspace. There is also an option to sync with Apple Reminders.*

:Author:
    David Young

:Date Created:
    November 15, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import codecs
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from tastic.tastic import document

# OR YOU CAN REMOVE THE CLASS BELOW AND ADD A WORKER FUNCTION ... SNIPPET TRIGGER BELOW
# xt-worker-def


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

        .. todo::

            - add usage info
            - create a sublime snippet for usage
            - update the package tutorial if needed

        .. code-block:: python 

            usage code   
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            workspaceRoot,
            workspaceName,
            syncFolder,
            settings=False
    ):
        self.log = log
        log.debug("instansiating a new 'sync' object")
        self.settings = settings
        self.workspaceRoot = workspaceRoot
        self.syncFolder = syncFolder
        self.workflowTags = self.settings["workflowTags"]
        syncTags = self.settings["syncTags"].replace("@", "").split(",")
        self.syncTags = []
        self.syncTags[:] = ["@" + s.strip() for s in syncTags]
        self.workspaceName = workspaceName

        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions
        # Recursively create missing directories
        if not os.path.exists(self.syncFolder):
            os.makedirs(self.syncFolder)

        return None

    def sync(self):
        """
        *sync the sync object*

        **Return:**
            - ``sync``

        **Usage:**
        .. todo::

            - add usage info
            - create a sublime snippet for usage
            - update the package tutorial if needed

        .. code-block:: python 

            usage code 
        """
        self.log.info('starting the ``sync`` method')

        taskpaperFiles = self._get_all_taskpaper_files(self.workspaceRoot)

        content = self.get_tagged_content_from_taskpaper_files(taskpaperFiles)
        if len(content):
            content = content.decode("utf-8")
            pathToWriteFile = self.syncFolder + "/" + self.workspaceName + ".taskpaper"
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToWriteFile,))
                writeFile = codecs.open(
                    pathToWriteFile, encoding='utf-8', mode='w')
            except IOError, e:
                message = 'could not open the file %s' % (pathToWriteFile,)
                self.log.critical(message)
                raise IOError(message)
            writeFile.write(content)
            writeFile.close()
            # OPEN TASKPAPER FILE
            doc = document(self.syncFolder + "/" +
                           self.workspaceName + ".taskpaper")
            doc.sort_projects(workflowTags=self.workflowTags)
            doc.sort_tasks(workflowTags=self.workflowTags)
            doc.save()

        # self.generate_sync_documents()

        self.log.info('completed the ``sync`` method')
        return None

    def generate_sync_documents(
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
        self.log.info('starting the ``generate_sync_documents`` method')

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

        self.log.info('completed the ``generate_sync_documents`` method')
        return None

    def _get_all_taskpaper_files(
            self,
            workspaceRoot):
        """*get a list of all the taskpaper filepaths in the workspace*

        **Key Arguments:**
            - ``workspaceRoot`` -- path to the root folder of a workspace containing taskpaper files
            -

        **Return:**
            - ``taskpaperFiles`` -- a list of paths to all the taskpaper files within the workspace
        """
        self.log.info('starting the ``_get_all_taskpaper_files`` method')

        from fundamentals.files import recursive_directory_listing
        theseFiles = recursive_directory_listing(
            log=self.log,
            baseFolderPath=self.workspaceRoot,
            whatToList="files"  # all | files | dirs
        )

        taskpaperFiles = []
        taskpaperFiles[:] = [f for f in theseFiles if os.path.splitext(f)[
            1] == ".taskpaper"]

        self.log.info('completed the ``_get_all_taskpaper_files`` method')
        return taskpaperFiles

    def get_tagged_content_from_taskpaper_files(
            self,
            taskpaperFiles):
        """*get tagged content from taskpaper files*

        **Key Arguments:**
            - ``tag`` -- the tag to search for
            - ``taskpaperFiles`` -- paths to all taskpaper files in workspace

        **Return:**
            - ``content`` -- the given tagged content of all taskpaper files in a workspace

        **Usage:**
            ..  todo::

                - add usage info
                - create a sublime snippet for usage
                - update package tutorial if needed

            .. code-block:: python 

                usage code 

        """
        self.log.info(
            'starting the ``get_tagged_content_from_taskpaper_files`` method')

        content = ""
        for tp in taskpaperFiles:
            # OPEN TASKPAPER FILE
            doc = document(tp)
            basename = os.path.basename(tp).replace("-", " ").upper()

            for tag in self.syncTags:
                filteredTasks = doc.tagged_tasks(tag)
                for ft in filteredTasks:
                    if "done" not in "".join(ft.tags):
                        content += ft.to_string() + "\n"

        self.log.info(
            'completed the ``get_tagged_content_from_taskpaper_files`` method')
        return content

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx

    # newContent = "- [%(title)s](dryx-open://%(tp)s) %(theseTags)s  \n" % locals()
