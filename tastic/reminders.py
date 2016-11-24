#!/usr/local/bin/python
# encoding: utf-8
"""
*methods for hooking up macOS/iOS reminds app tasks with taskpaper docs*

:Author:
    David Young

:Date Created:
    November 22, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from subprocess import Popen, PIPE, STDOUT
from . import workspace
import codecs


class reminders():
    """
    *the taskpaper reminders object*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_).

        To initiate a reminders object, use the following:

        .. code-block:: python

            from tastic import reminders
            r = reminders(
                log=log,
                settings=settings
            )
    """
    # INITIALISATION

    def __init__(
            self,
            log,
            settings=False,

    ):
        self.log = log
        log.debug("instansiating a new 'reminders' object")
        self.settings = settings
        # xt-self-arg-tmpx

        return None

    def import_list(
        self,
        listName,
        pathToTaskpaperDoc
    ):
        """
        *import tasks from a reminder.app list into a given taskpaper document*

        **Key Arguments:**
            - ``listName`` -- the name of the reminders list
            - ``pathToTaskpaperDoc`` -- the path to the taskpaper document to import the tasks into

        **Usage:**

            The following will import tasks from a Reminder.app list into a taskpaper document. Tasks are added to any existing content in the taskpaper document, or if the docuement doesn't yet exist it will be created for you. Tasks are deleted from the remainds list once import is complete.

            .. code-block:: python

                r.import_list(
                    listName="listname",
                    pathToTaskpaperDoc="/path/to/my/doc.taskpaper"
                )
        """

        self.log.info('starting the ``import_list`` method')

        newTasks = self._get_tasks_from_reminder_list(listName)
        self._add_tasks_to_taskpaper(
            pathToTaskpaperDoc=pathToTaskpaperDoc,
            taskString=newTasks
        )
        self._delete_reminders_from_list(
            listName=listName
        )

        self.log.info('completed the ``import_list`` method')
        return newTasks

    def _get_tasks_from_reminder_list(
            self,
            listName):
        """*get the tasks from a reminder app list as a string in taskpaper format*

        **Key Arguments:**
            - ``listName`` -- the name of the reminders list

        **Return:**
            - ``newTasks`` -- a string containing tasks in taskpaper format
        """
        self.log.info('starting the ``_get_tasks_from_reminder_list`` method')

        from subprocess import Popen, PIPE, STDOUT
        applescript = """
            tell application "Reminders"
                --set output to name of reminders
                set myList to "%(listName)s"
                if (count of (reminders in list myList whose completed is false)) > 0 then
                    set todoListNames to name of reminders in list myList whose completed is false
                    set todoListNotes to body of reminders in list myList whose completed is false
                    set todoListDates to due date of reminders in list myList whose completed is false
                    set output to ""
                    repeat with itemNum from 1 to (count of todoListNames)
                        set output to output & "- " & (item itemNum of todoListNames)
                        if (item itemNum of todoListDates) > date "Tuesday, 25 December 1900 at 00:00:00" then
                            set dueDate to my date_time_to_iso(item itemNum of todoListDates)
                            set output to output & " @due(" & dueDate & ")"
                        end if
                        set output to output & return
                        if item itemNum of todoListNotes exists then
                            repeat with para in every paragraph of (item itemNum of todoListNotes)
                                set output to (output & "    " & para as string) & return
                            end repeat
                        end if
                    end repeat
                else
                    set output to ""
                end if
                return output
            end tell

            on date_time_to_iso(dt)
                set {year:y, month:m, day:d, hours:h, minutes:min, seconds:s} to dt
                set y to text 2 through -1 of ((y + 10000) as text)
                set m to text 2 through -1 of ((m + 100) as text)
                set d to text 2 through -1 of ((d + 100) as text)
                set h to text 2 through -1 of ((h + 100) as text)
                set min to text 2 through -1 of ((min + 100) as text)
                set s to text 2 through -1 of ((s + 100) as text)
                return y & "-" & m & "-" & d & " " & h & ":" & min
            end date_time_to_iso
        """ % locals()
        cmd = "\n".join(["osascript << EOT", applescript, "EOT"])
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        self.log.debug('output: %(stdout)s' % locals())
        newTasks = stdout.decode("utf-8")
        if len(stderr):
            self.log.error(stderr)
            sys.exit(0)

        self.log.info('completed the ``_get_tasks_from_reminder_list`` method')
        return newTasks

    def _add_tasks_to_taskpaper(
        self,
        pathToTaskpaperDoc,
        taskString
    ):
        """*add the tasks to a taskpaper document*

        **Key Arguments:**
            - ``pathToTaskpaperDoc`` -- the path to the taskpaper document to import the tasks into
            - ``taskString`` -- a string containing tasks in taskpaper format
        """
        self.log.info('starting the ``_add_tasks_to_taskpaper`` method')

        exists = os.path.exists(pathToTaskpaperDoc)
        thisData = ""
        if exists:
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToTaskpaperDoc,))
                readFile = codecs.open(
                    pathToTaskpaperDoc, encoding='utf-8', mode='r')
                thisData = readFile.read()
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToTaskpaperDoc,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()

        thisData = taskString + "\n" + thisData

        try:
            self.log.debug("attempting to open the file %s" %
                           (pathToTaskpaperDoc,))
            writeFile = codecs.open(
                pathToTaskpaperDoc, encoding='utf-8', mode='w')
        except IOError, e:
            message = 'could not open the file %s' % (pathToTaskpaperDoc,)
            self.log.critical(message)
            raise IOError(message)
        writeFile.write(thisData)
        writeFile.close()

        ws = workspace(
            log=self.log,
            settings=self.settings,
            fileOrWorkspacePath=pathToTaskpaperDoc
        )
        ws.sort()

        self.log.info('completed the ``_add_tasks_to_taskpaper`` method')
        return None

    def _delete_reminders_from_list(
            self,
            listName):
        """* delete reminders from list*

        **Key Arguments:**
            - ``listName`` -- the name of the reminders list
        """
        self.log.info('starting the ``_delete_reminders_from_list`` method')

        applescript = """
            tell application "Reminders"
                -- Loop thru reminders in the targeted reminder.app list
                tell list "%(listName)s"
                    set theTasks to every reminder
                    repeat with theTask in theTasks
                            delete theTask
                    end repeat
                end tell
            end tell
        """ % locals()
        cmd = "\n".join(["osascript << EOT", applescript, "EOT"])
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()

        if len(stderr):
            self.log.error(stderr)
            sys.exit(0)

        self.log.info('completed the ``_delete_reminders_from_list`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
