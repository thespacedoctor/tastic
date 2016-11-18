#!/usr/local/bin/python
# encoding: utf-8
"""
*A library of tools for working with plain-text taskpaper documents*

:Authors:
    @thespacedoctor

:Date Created:
    September  2, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import re
import codecs
import collections
from datetime import datetime, date, time


class baseClass():
    """
    *This is the base class for all taskpaper objects: documents, projects and tasks*

    **Key Arguments:**
        - ``matchObject`` -- a dictionary containing the constituent parts of the object
        - ``parentObject`` -- the parent object containing this taskpaper object. Default *None*
    """

    def __init__(self, matchObject, parentObject=None):
        self.meta = matchObject
        if self.meta["content"] == None:
            self.meta["content"] = ""
        self.parent = parentObject

    @property
    def raw_content(
            self):
        """*The raw, untidied content of the taskpaper object*

        **Usage:**

            To return the inital raw content for the matched object (document, project, task or note)

            .. code-block:: python

                print project.raw_content
                print note.raw_content
                print task.raw_content
        """
        return self.meta["raw_content"]

    @property
    def projects(self):
        """*All child projects of this taskpaper object*

        **Usage:**

            Given a taskpaper document object (`doc`), to get a list of the project objects found within the document use:

            .. code-block:: python

                docProjects = doc.projects

            The same is true of project objects which may contain sub-projects:

            .. code-block:: python

                aProject = docProjects[0]
                subProjects = aProject.projects
        """
        return self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>(?!\[Searches\]|- )\S.*?:(?!\S)) *(?P<tagString>( *?@[^(\s]+(\([^)]*\))?)+)?(?P<content>(\n(( |\t)+\S.*)|\n( |\t)*|\n)+)', re.UNICODE),
            objectType="project",
            content=None
        )

    @property
    def tasks(self):
        """*list of the tasks assoicated with this object*

        **Usage:**

            Given a taskpaper document object (`doc`), get a list of top-level tasks associated with the document using:

            .. code-block:: python

                docTasks = doc.tasks

            The same is true of project and task objects that may contain sub-tasks:

            .. code-block:: python

                aProject.tasks
                aTasks.tasks
        """
        return self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>- ((?! @).)*)( *(?P<tagString>( *?@[^(\s]+(\([^)]*\))?)+))?(?P<content>(\n(( |\t)+\S.*)|\n( |\t)*)*)', re.UNICODE),
            objectType="task",
            content=None
        )

    @property
    def content(
            self):
        """*The text content of this object (excluding title)*

        Much like the `raw_content` of an object, but does not include a title or tags. The initial indentation is also removed. For a document object the `content` is synonymous with `raw_content`.

        **Usage:**

            .. code-block:: python

                pContent = aProject.content
                tContent = aTask.content
        """
        reIndent = re.compile(r'^(?P<indent>\s+).*?$', re.UNICODE)

        cleanedContent = ""
        replaceContent = ""

        # FIND THE SMALLEST INDENT LEVEL IN THE CONTENT
        lowestIndent = "\t" * 10
        for line in self.meta["content"].split("\n"):
            if len(line.strip()) == 0:
                continue
            matchObject = reIndent.match(line)
            if matchObject:
                indent = matchObject.group("indent")
                if len(indent) < len(lowestIndent):
                    lowestIndent = indent

        # STRIP OFF THE SMALLEST INDENT LEVEL FROM CONTENT
        for line in self.meta["content"].split("\n"):
            if len(line.strip()) == 0:
                continue
            cleanedContent += line[len(lowestIndent):] + "\n"
            replaceContent += line + "\n"

        self.meta["content"] = replaceContent[:-1]
        return cleanedContent[:-1]

    @property
    def title(
            self):
        """*The title of this taskpaper object*

        **Usage:**

            .. code-block:: python

                aProject.title
                aTasks.title
                aNote.title
        """

        return self.meta["title"]

    @property
    def tags(
            self):
        """*The list of tags associated with this taskpaper object*

        **Usage:**
            ..
            project and task objects can have associated tags. To get a list of tags assigned to an object use:

            .. code-block:: python

                projectTag = aProject.tags
                taskTags = aTasks.tags

                print projectTag
                > ['flag', 'home(bathroom)']
        """

        tags = []
        regex = re.compile(r'@[^@]*', re.S)
        if self.meta["tagString"]:
            matchList = regex.findall(self.meta["tagString"])
            for m in matchList:
                tags.append(m.strip().replace("@", ""))

        return tags

    @property
    def notes(self):
        """*list of the notes assoicated with this object*

        **Usage:**

            The document, project and task objects can all contain notes.

            .. code-block:: python

                docNotes = doc.notes
                projectNotes = aProject.notes
                taskNotes = aTask.notes
        """
        return self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>\S(?<!-)((?!(: +@|: *\n|: *$)).)*)\s*?(\n|$)(?P<tagString>&&&)?(?P<content>&&&)?', re.UNICODE),
            objectType="note",
            content=None
        )

    @property
    def parent(
            self):
        """*This taskpaper object's parent object (if any)*

        **Usage:**

            To reserve up the taskpaper document tree and find the parent object
            that contains this object (e.g. the document containing the task you're working with) use the following:

            .. code-block:: python

                taskParent = aTasks.parent
                print taskParent

            prints the following

            .. code-block:: text

                <Taskpaper Document `saturday-tasks.taskpaper`>
        """

        return self.parent

    def get_project(
            self,
            projectName):
        """*recursively scan this taskpaper object to find a descendant project by name*

        **Key Arguments:**
            - ``projectName`` -- the name, or title, of the project you want to return

        **Return:**
            - ``project`` -- the taskpaper project object you requested (or ``None`` if no project was matched)

        **Usage:**

            .. code-block:: python

                archiveProject = doc.get_project("Archive")
        """

        if projectName[-1] != ":":
            projectName += ":"
        project = None
        for p in self.projects:
            if p.title.lower() == projectName.lower():
                project = p
                break

        if project == None:
            for p in self.projects:
                project = p.get_project(projectName)
                if project:
                    break

        return project

    def get_task(
            self,
            taskName):
        """*recursively scan this taskpaper object to find a descendant task by name*

        **Key Arguments:**
            - ``taskName`` -- the name, or title, of the task you want to return

        **Return:**
            - ``task`` -- the taskpaper task object you requested (or ``None`` if no task was matched)

        **Usage:**

            .. code-block:: python

                aTask = doc.get_task("cut the grass")
        """

        if taskName[:2] != "- ":
            taskName = "- " + taskName
        task = None
        try:
            self.refresh
        except:
            pass
        for t in self.tasks:
            if t.title.lower() == taskName.lower() and task == None:
                task = t
                break

        if task == None:
            for p in self.projects:
                p.refresh
                for t in p.tasks:
                    if t.title.lower() == taskName.lower() and task == None:
                        task = t
                        break

        if task == None:
            for p in self.projects:
                task = p.get_task(taskName)
                if task:
                    break
        return task

    def to_string(
            self,
            indentLevel=1,
            title=True,
            tags=None,
            projects=None,
            tasks=None,
            notes=None):
        """*convert this taskpaper object to a string*

        **Key Arguments:**
            - ``indentLevel`` -- the level of the indent for this object. Default *1*.
            - ``title`` -- print the title of the taskpaper object alongside the contents. Default *True*
            - ``tags`` -- replace tags with these tags. Default *None*
            - ``projects`` -- replace projects with these projects, pass empty list to delete all projects. Default *None*
            - ``tasks`` -- replace tasks with these ones, pass empty list to delete all tasks. Default *None*
            - ``notes`` -- replace notes with these ones, pass empty list to delete all notes. Default *None*

        **Return:**
            - ``objectString`` -- the taskpaper object as a string

        **Usage:**

            If we have the *archive* project from a taskpaper document, we can convert it to a string using:

            .. code-block:: python

                print archiveProject.to_string()

            .. code-block:: text

                Archive:
                    - and a third task @done(2016-09-04) @project(parent project / child-project)
                    - and a forth task @done(2016-09-04) @project(parent project / child-project)
                    - fill the kettle @done(2016-09-04) @project(parent project / make coffee)
                    - boil the kettle @done(2016-09-04) @project(parent project / make coffee)
        """
        indent = indentLevel * "\t"

        objectString = ""
        if title:
            try:
                # NONE DOCUMENT OBJECTS
                objectString += self.title
            except:
                pass

            try:
                if tags:
                    tagString = (" @").join(tags)
                else:
                    tagString = (" @").join(self.tags)

                if len(tagString):
                    objectString += " @" + tagString
            except:
                pass

        try:
            if not notes:
                notes = self.notes
            for n in notes:
                if len(n.title.strip()):
                    if not self.parent and len(objectString) == 0:
                        objectString += indent + n.title.strip() + n.content
                    else:
                        objectString += "\n" + indent + n.title.strip() + n.content
        except:
            pass

        try:
            if not tasks:
                tasks = self.tasks
            for t in tasks:
                objectString += "\n" + indent + t.to_string(indentLevel + 1)
        except:
            pass

        try:
            if not projects:
                projects = self.projects
            for p in projects:
                objectString += "\n" + indent + p.to_string(indentLevel + 1)
        except:
            pass

        try:
            objectString += "\n" + indent + self.searches
        except:
            pass

        return objectString.strip()

    def tagged_projects(
            self,
            tag):
        """*return a list of projects contained within this taskpaper object filtered by a given tag*

        **Key Arguments:**
            - ``tag`` -- the tag to filter the projects by.

        **Return:**
            - ``projectList`` -- the list of filtered projects

        **Usage:**

            To filter the projects recursively found with a taskpaper document object and return only those projects tagged with ``flag``, using the following:

            .. code-block:: python

                filteredProjects = doc.tagged_projects("flag")
                for p in filteredProjects:
                    print p.title

            Note you can give the tag with or without the *@*, and you can also give a tag attribute, e.g. ``@due(today)``
        """
        self.refresh
        projectList = []
        tag = tag.replace("@", "").lower()
        for p in self.projects:
            for aTag in p.tags:
                if "(" not in tag:
                    aTag = aTag.split("(")[0]
                if aTag.lower() == tag:
                    projectList.append(p)
                    break

            subProjects = p.tagged_projects(tag)
            projectList += subProjects

        return projectList

    def tagged_tasks(
            self,
            tag):
        """*return a list of tasks contained within this taskpaper object filtered by a given tag*

        **Key Arguments:**
            - ``tag`` -- the tag to filter the tasks by.

        **Return:**
            - ``taskList`` -- the list of filtered tasks

        **Usage:**

            To filter the tasks recursively found with a taskpaper document object and return only those tasks tagged with ``flag``, using the following:

            .. code-block:: python

               filteredTasks = doc.tagged_tasks("@flag")
               for t in filteredTasks:
                    print t.title

            Note you can give the tag with or without the *@*, and you can also give a tag attribute, e.g. ``@due(today)``
        """
        self.refresh
        tasksList = []
        tag = tag.replace("@", "").lower()
        for t in self.tasks:
            for aTag in t.tags:
                if "(" not in tag:
                    aTag = aTag.split("(")[0]
                if aTag.lower() == tag:
                    tasksList.append(t)
                    break

            subtasks = t.tagged_tasks(tag)
            tasksList += subtasks

        isProject = False
        try:
            this = self.projects
            isProject = True
        except:
            pass

        if isProject:
            for p in self.projects:
                subtasks = p.tagged_tasks(tag)
                tasksList += subtasks

        return tasksList

    def sort_projects(
            self,
            workflowTags):
        """*order the projects within this taskpaper object via a list of tags*

         The order of the tags in the list dictates the order of the sort - first comes first*

        **Key Arguments:**
            - ``workflowTags`` -- a string of space/comma seperated tags.

        **Return:**
            - ``None``

        **Usage:**

            To recursively sort the projects within a taskpaper document with the following order:

            1. *@due*
            2. *@flag*
            3. *@hold*
            4. *@next*
            5. *@someday*
            6. *@wait*

            use the following:

            .. code-block:: python

                doc.sort_projects("@due, @flag, @hold, @next, @someday, @wait")
        """
        self.refresh
        workflowTagsLists = workflowTags.strip().replace(",", "").replace("@", "")
        workflowTagsLists = workflowTagsLists.split(" ")
        matchedProjects = collections.OrderedDict()
        unmatchedProjects = []
        for wt in workflowTagsLists:
            matchedProjects[wt.lower()] = []
        for p in self.projects:
            matched = False
            for pt in p.tags:
                if matched:
                    break
                for wt in workflowTagsLists:
                    thisTag = pt.lower()
                    if "(" not in wt:
                        thisTag = pt.split("(")[0].lower()
                    if thisTag == wt.lower() and matched == False:
                        matchedProjects[wt.lower()].append(p)
                        matched = True
                        break
            if matched == False:
                unmatchedProjects.append(p)

        sortedProjects = []
        for k, v in matchedProjects.iteritems():
            sortedProjects += v

        sortedProjects += unmatchedProjects
        self.projects = sortedProjects

        self.content = self.to_string(
            title=False, projects=sortedProjects, indentLevel=0)

        for p in self.projects:
            p.projects = p.sort_projects(workflowTags)

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        oldContent = self.to_string(indentLevel=1)
        newContent = self.to_string(
            indentLevel=1, projects=sortedProjects)

        if self.parent:
            self.parent._update_document_tree(
                oldContent=oldContent,
                newContent=newContent
            )

        self.content = self.content.replace(self.to_string(indentLevel=0, title=False), self.to_string(
            indentLevel=0, title=False, projects=sortedProjects))

        self.refresh

        return sortedProjects

    def sort_tasks(
            self,
            workflowTags,
            indentLevel=1):
        """*order tasks within this taskpaper object via a list of tags*

        The order of the tags in the list dictates the order of the sort - first comes first*

        **Key Arguments:**
            - ``workflowTags`` -- a string of space seperated tags.

        **Return:**
            - ``None``

        **Usage:**

            To recursively sort the tasks within a taskpaper document with the following order:

            1. *@due*
            2. *@flag*
            3. *@hold*
            4. *@next*
            5. *@someday*
            6. *@wait*

            use the following:

            .. code-block:: python

                doc.sort_tasks("@due, @flag, @hold, @next, @someday, @wait")
        """
        self.refresh
        workflowTagsLists = workflowTags.strip().replace(",", "").replace("@", "")
        workflowTagsLists = workflowTagsLists.split(" ")
        matchedTasks = collections.OrderedDict(sorted({}.items()))
        unmatchedTasks = []

        for wt in workflowTagsLists:
            matchedTasks[wt.lower()] = []
        for t in self.tasks:
            matched = False
            for tt in t.tags:
                if matched:
                    break
                for wt in workflowTagsLists:
                    thisTag = tt.lower()
                    if "(" not in wt:
                        thisTag = tt.split("(")[0].lower()
                    if thisTag == wt.lower() and matched == False:
                        matchedTasks[wt.lower()].append(t)
                        matched = True
                        break
            if matched == False:
                unmatchedTasks.append(t)

        sortedTasks = []
        for k, v in matchedTasks.iteritems():
            sortedTasks += v

        oldContent = self.to_string(indentLevel=1)
        sortedTasks += unmatchedTasks
        self.tasks = sortedTasks

        self.content = self.to_string(
            title=False, tasks=sortedTasks, indentLevel=0)

        hasProjects = False
        try:
            this = self.projects
            hasProjects = True
        except:
            pass

        if hasProjects:
            for p in self.projects:
                p.tasks = p.sort_tasks(workflowTags, 1)

        for t in self.tasks:
            t.tasks = t.sort_tasks(workflowTags, 1)

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        newContent = self.to_string(
            tasks=sortedTasks, indentLevel=1)

        if self.parent:
            self.parent._update_document_tree(
                oldContent=oldContent,
                newContent=newContent
            )

        self.content = self.content.replace(self.to_string(indentLevel=0, title=False), self.to_string(
            indentLevel=0, title=False, tasks=sortedTasks))

        self.refresh
        return sortedTasks

    def _get_object(
        self,
        regex,
        objectType,
        content=None
    ):
        # INITIATE THE OBJECTS LIST
        objectList = []

        # READ THE CONTENT OF THE PARENT OBJECT
        if not content:
            content = self.content

        # FIND ALL OCCURANCE OF THE REGEX IN CONTENT

        thisIter = regex.finditer(content)
        for item in thisIter:
            match = {
                "title": item.group("title"),
                "tagString": item.group("tagString"),
                "content": item.group("content"),
                "startIndex": item.start(),
                "endIndex": item.end(),
                "raw_content": item.group()
            }
            if objectType == "project":
                objectList.append(project(match, self))
            if objectType == "note":
                objectList.append(note(match, self))
            if objectType == "task":
                objectList.append(task(match, self))
            if objectType == "searchBlock":
                objectList = item.group()

        return objectList

    def tidy(self):
        """*Tidy this taskpapaer object so that sub-objects appear in this order: title, tags, notes, tasks, projects*

        **Return:**
            - ``None``

        **Usage:**

           When a taskpaper document is opened it is tidied by default. To tidy the document object (or project or task) use the command:

            .. code-block:: python

                doc.tidy()
        """
        try:
            self.tags.sort(lambda x, y: cmp(len(x), len(y)))
        except:
            pass

        try:
            for t in self.tasks:
                t.tidy()
        except:
            pass

        try:
            for p in self.projects:
                p.tidy()
        except:
            pass

        # REMOVE BLANK LINES
        if self.content:
            if self.parent:
                self.content = ("\n").join(self.to_string(
                    indentLevel=0).split("\n")[1:])
            else:
                regex = re.compile(r'\s*?\n\s*?\n')
                while "\n\n" in self.content:
                    self.content = regex.sub("\n", self.content)
        return None

    def add_project(
            self,
            title,
            tags=None):
        """*Add a project to this taskpaper object*

        **Key Arguments:**
            - ``title`` -- the title for the project.
            - ``tags`` -- tag string (*"@one @two(data)"*) or list of tags (*['one', 'two(data)']*)
            - ``oldContent`` -- the old content to be replaced in parent object (user sould not need to give this)
            - ``newContent`` -- the replacement text for the parent object  (user sould not need to give this)

        **Return:**
            - ``project`` -- the new taskpaper project object

        **Usage:**

            To add a sub-project to a taskpaper document or project use:

            .. code-block:: python

                newProject = doc.add_project(
                    title="this is a projects I added",
                    tags="@with @tags"
                )
        """
        self.refresh
        project = title.strip()
        if ":" != project[-1]:
            project += ":"

        if tags:
            if isinstance(tags, list):
                if "@" not in tags[0]:
                    tagString = (" @").join(tags)
                    tagString = "@" + tagString
                else:
                    tagString = (" ").join(tags)
            else:
                tagString = tags

            tagString = tagString.strip()
            project += " " + tagString

        newProject = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>(?!\[Searches\]|- )\S.*?:(?!\S)) *(?P<tagString>( *?@[^(\s]+(\([^)]*\))?)+)?(?P<content>(\n(( |\t)+\S.*)|\n( |\t)*|\n)+)', re.UNICODE),
            objectType="project",
            content=project
        )

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        oldContent = self.to_string(indentLevel=1)
        newContent = self.to_string(
            indentLevel=1, projects=self.projects + newProject)

        if self.parent:
            doc = self.parent._update_document_tree(
                oldContent=oldContent,
                newContent=newContent
            )

        self.content = self.content.replace(self.to_string(indentLevel=0, title=False), self.to_string(
            indentLevel=0, title=False, projects=self.projects + newProject))

        doc = self
        while doc.parent:
            doc = doc.parent
        doc.refresh

        if not self.parent:
            parent = self
        else:
            parent = doc.get_project(self.title)

        thisProject = parent.get_project(title)

        self.refresh
        return thisProject

    def _update_document_tree(
            self,
            oldContent=None,
            newContent=None):
        """*update document tree*

        **Key Arguments:**
            - ``oldContent`` -- the old content to be replaced in parent object (user sould not need to give this)
            - ``newContent`` -- the replacement text for the parent object  (user sould not need to give this)

        **Return:**
            - ``doc`` -- the updated document object
        """
        self.refresh
        if self.parent:
            self.refresh
            indentOldContent = ""
            indentNewContent = ""
            for l in oldContent.split("\n"):
                indentOldContent += "\t" + l + "\n"
            uoldContent = indentOldContent[:-1]
            for l in newContent.split("\n"):
                indentNewContent += "\t" + l + "\n"
            unewContent = indentNewContent[:-1]

            thisOldContent = self.to_string(indentLevel=1)
            thisNewContent = thisOldContent.replace(uoldContent, unewContent)
            self.content = self.to_string(
                indentLevel=0, title=False).replace(oldContent, newContent)

            self.content = self.to_string(
                indentLevel=0, title=False).replace(oldContent, newContent)

            # REPLACE THE NEW CONTENT OF THIS PROJECT IN THE PARENT OBJECT'S
            # CONTENT
            doc = self.parent._update_document_tree(
                oldContent=thisOldContent,
                newContent=thisNewContent
            )

        else:
            self.content = self.content.replace(oldContent, newContent)
            doc = self

        self.refresh
        return doc

    def add_tag(
            self,
            tag):
        """*Add a tag this taskpaper object*

        **Key Arguments:**
            - ``tag`` -- the tag to add to the object

        **Usage:**

            .. code-block:: python 

                aTask.add_tag("@due")
        """

        self.refresh
        oldContent = self.to_string(indentLevel=1)
        self.tags += [tag.replace("@", "")]
        newContent = self.to_string(indentLevel=1)

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        self.parent._update_document_tree(
            oldContent=oldContent,
            newContent=newContent
        )

        self.refresh
        return None

    def set_tags(
            self,
            tags=""):
        """*Set the tags for this taskpaper object*

        **Key Arguments:**
            - ``tags`` -- a tag string to set

        **Usage:**

            .. code-block:: python 

                aTask.set_tags("@due @mac")
        """
        self.refresh
        tagList = []
        regex = re.compile(r'@[^@]*', re.S)
        matchList = regex.findall(tags)
        for m in matchList:
            tagList.append(m.strip().replace("@", ""))

        self.refresh
        oldContent = self.to_string(indentLevel=1)
        self.tags = tagList
        newContent = self.to_string(indentLevel=1)

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        self.parent._update_document_tree(
            oldContent=oldContent,
            newContent=newContent
        )
        self.refresh
        return None

    def done(
            self,
            depth="root"):
        """*mark this object as done*

        **Key Arguments:**
            - ``depth`` -- either mark root item as done or all recursive items. Default *"root"*. ["root"|"all"]

        **Usage:**

            To mark a task or project as done"

            .. code-block:: python

                aTask.done()

            Or or mark the object as done as well all descendant tasks and projects:

            .. code-block:: python

                aTask.done("all")
        """
        self.refresh
        oldContent = self.to_string(indentLevel=1)
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        newContent = self.to_string(
            indentLevel=1, tags=["done(%(now)s)" % locals()])

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        self.parent._update_document_tree(
            oldContent=oldContent,
            newContent=newContent
        )

        self.tags = ["done(%(now)s)" % locals()]

        if depth == "all":
            try:
                for t in self.tasks:
                    t.done("all")
            except:
                pass

            try:
                for p in self.projects:
                    t.done("all")
            except:
                pass

        self.refresh

        return self

    def notestr(
            self):
        """*return the notes of this object as a string*

        **Return:**
            - ``notestr`` -- the notes as a string

        **Usage:**

            .. code-block:: python 

                doc.notestr
        """
        self.refresh
        notestr = ""

        for n in self.notes:
            if len(n.title.strip()):
                notestr += "\n" + n.title.strip() + n.content

        return notestr

    def add_task(
            self,
            title,
            tags=None):
        """*Add a task to this taskpaper object*

        **Key Arguments:**
            - ``title`` -- the title for the task.
            - ``tags`` -- tag string (*'@one @two(data)'*) or list of tags (*['one', 'two(data)']*)

        **Return:**
            - ``task`` -- the new taskpaper task object

        **Usage:**

            To add a task to an object (document, project, or task) use:

            .. code-block:: python

                newTask = doc.add_task("this is a task I added", "@with @tags")
        """
        self.refresh
        task = title.strip()
        if task[:2] != "- ":
            task = "- " + task

        if tags:
            if isinstance(tags, list):
                if "@" not in tags[0]:
                    tagString = (" @").join(tags)
                    tagString = "@" + tagString
                else:
                    tagString = (" ").join(tags)
            else:
                tagString = tags

            tagString = tagString.strip()
            task += " " + tagString

        newTask = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>- ((?! @).)*)( *(?P<tagString>( *?@[^(\s]+(\([^)]*\))?)+))?(?P<content>(\n(( |\t)+\S.*)|\n( |\t)*)*)', re.UNICODE),
            objectType="task",
            content=task
        )

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        oldContent = self.to_string(indentLevel=1)
        newContent = self.to_string(
            indentLevel=1, tasks=self.tasks + newTask)

        if self.parent:
            doc = self.parent._update_document_tree(
                oldContent=oldContent,
                newContent=newContent
            )

        self.content = self.content.replace(self.to_string(indentLevel=0, title=False), self.to_string(
            indentLevel=0, title=False, tasks=self.tasks + newTask))

        print self.parent
        doc = self
        while doc.parent:
            doc = doc.parent
        doc.refresh

        if not self.parent:
            parent = self
        else:

            parent = doc.get_project(self.title)
        if not parent:
            parent = doc.get_task(self.title)

        print parent
        thisTask = parent.get_task(title)

        self.refresh

        return thisTask

    def add_note(
            self,
            note):
        """*Add a note to this taskpaper object*

        **Key Arguments:**
            - ``note`` -- the note (string)

        **Return:**
            - None

        **Usage:**

            To add a note to a document, project or task object:

            .. code-block:: python

                newNote = doc.add_note(And another note with a link http://www.thespacedoctor.co.uk")
        """
        self.refresh
        note = note.strip()

        newNote = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>\S(?<!-)((?!(: +@|: *\n|: *$)).)*)\s*?(\n|$)(?P<tagString>&&&)?(?P<content>&&&)?', re.UNICODE),
            objectType="note",
            content=note
        )

        # ADD DIRECTLY TO CONTENT IF THE PROJECT IS BEING ADDED SPECIFICALLY TO
        # THIS OBJECT
        oldContent = self.to_string(indentLevel=1)
        newContent = self.to_string(
            indentLevel=1, notes=self.notes + newNote)

        if self.parent:
            self.parent._update_document_tree(
                oldContent=oldContent,
                newContent=newContent
            )

        self.content = self.content.replace(self.to_string(indentLevel=0, title=False), self.to_string(
            indentLevel=0, title=False, notes=self.notes + newNote))

        doc = self
        while doc.parent:
            doc = doc.parent
        doc.refresh

        self.refresh

        return newNote[0]


class document(baseClass):
    """
    *This is the taskpaper document object - top level object*

    **Key Arguments:**
        - ``filepath`` -- path to the taskpaper document

    **Usage:**

            To read a taskpaper document, use something like this:

            .. code-block:: python

                # READ IN A TASKPAPER FILE
                from tastic.tastic import document
                taskpaperFile = "path/to/saturday-tasks.taskpaper"
                doc = document(taskpaperFile)

            Note that tastic will tidy the contents of the file when it is read into memory. See the `tidy()` method for details.
    """

    def __init__(self, filepath, parentObject=None):
        self.filepath = filepath
        self.raw_content = self._get_raw_content()
        self.content = self.raw_content
        self.level = -1
        self.parent = None
        self.filename = os.path.basename(self.filepath)

    def __repr__(self):
        return "<Taskpaper Document `%s`>" % self.filename

    @property
    def raw_content(
            self):
        """*The raw, untidied content of this taskpaper document*

        **Usage:**

            .. code-block:: python

                # DISPLAY THE RAW CONTENT OF THE DOCUMENT
                print doc.raw_content
        """
        return self.raw_content

    def _get_raw_content(self):

        readFile = codecs.open(self.filepath, encoding='utf-8', mode='r')
        content = readFile.read()
        readFile.close()

        return content.encode("utf-8")

    @property
    def tags(self):
        """*document objects have no tags*"""
        raise AttributeError("document object has no tags attribute")

    @property
    def searches(self):
        """*The search-block (if any) associated with this document*

        **Usage:**

            .. code-block:: python

                # DOCUMENT SEARCHES
                docSearchBlock = doc.searches
        """
        return self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>\[Searches\]:) *(?P<tagString>( *?@\S*(\(.*?\))?)+)?(?P<content>(\n( |\t).*)*)', re.UNICODE),
            objectType="searchBlock",
            content=None
        )

    def save(
            self,
            copypath=None):
        """*save the content of the document back to the file*

        **Key Arguments:**
            - ``copypath`` -- the path to a new file if you want to make a copy of the document instead of saving it to the original filepath. Default *None*


        **Usage:**

            To save the document to file run:

            .. code-block:: python

                doc.save()

            Or to copy the content to another file run the save method with a new filepath as an argument:

            .. code-block:: python

                doc.save("/path/to/saturday-tasks-copy.taskpaper")
        """
        self.refresh
        if copypath:
            self.filepath = copypath

        content = self.content

        import codecs
        # SET ENCODE ERROR RETURN VALUE

        def handler(e):
            return (u' ', e.start + 1)
        codecs.register_error('dryx', handler)

        # RECODE INTO ASCII
        udata = content.decode("utf-8")
        content = udata.encode("ascii", "dryx")

        writeFile = codecs.open(self.filepath, encoding='utf-8', mode='w')
        writeFile.write(content)
        writeFile.close()

        return None

    @property
    def refresh(
            self):
        """*Refreshs this documents's attributesd*

        **Usage:**

            To refresh the taskpaper document:

            .. code-block:: python

                doc.refresh
        """

        self.projects = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>(?!\[Searches\]|- )\S.*?:(?!\S)) *(?P<tagString>( *?@[^(\s]+(\([^)]*\))?)+)?(?P<content>(\n(( |\t)+\S.*)|\n( |\t)*|\n)+)', re.UNICODE),
            objectType="project",
            content=None
        )

        self.tasks = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>- ((?! @).)*)( *(?P<tagString>( *?@[^(\s]+(\([^)]*\))?)+))?(?P<content>(\n(( |\t)+\S.*)|\n( |\t)*)*)', re.UNICODE),
            objectType="task",
            content=None
        )

        self.notes = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>\S(?<!-)((?!(: +@|: *\n|: *$)).)*)\s*?(\n|$)(?P<tagString>&&&)?(?P<content>&&&)?', re.UNICODE),
            objectType="note",
            content=None
        )

        self.search = self._get_object(
            regex=re.compile(
                r'((?<=\n)|(?<=^))(?P<title>\[Searches\]:) *(?P<tagString>( *?@\S*(\(.*?\))?)+)?(?P<content>(\n( |\t).*)*)', re.UNICODE),
            objectType="searchBlock",
            content=None
        )

        return None

    def set_tags(self):
        raise AttributeError("document object has no 'set_tags' method")

    def add_tag(self):
        raise AttributeError("document object has no 'add_tag' method")

    def done(self):
        raise AttributeError("document object has no 'done' method")


class task(baseClass):
    """
    *The taskpaper task object*
    """

    def __repr__(self):
        return "<Task `%s` (%s)>" % (self.title, self.tags)

    @property
    def projects(self):
        return []

    @property
    def refresh(
            self):
        """*Refreshs this tasks's attributes if, for example, the parent document's projects or tasks has been sorted*

        **Usage:**

            To refresh the task:

            .. code-block:: python

                aTask.refresh
        """

        if self.parent:
            self.parent.refresh

        replace = None
        title = self.title
        for t in self.parent.tasks:
            if t.title == title:
                replace = t
        if not replace:
            return
        self.tags = replace.tags
        self.notes = replace.notes
        self.tasks = replace.tasks

        self.content = replace.to_string(indentLevel=0, title=False)

        return None

    @property
    def projects(self):
        raise AttributeError("task object has no attribute 'projects'")

    def get_project(self):
        raise AttributeError("task object has no 'get_project' method")

    def tagged_projects(self):
        raise AttributeError("task object has no 'tagged_projects' method")

    def sort_projects(self):
        raise AttributeError("task object has no 'sort_projects' method")

    def add_project(self):
        raise AttributeError("task object has no 'add_project' method")


class project(baseClass):
    """
    *The taskpaper project object*
    """

    def __repr__(self):
        return "<Project `%s`>" % self.title

    @property
    def refresh(
            self):
        """*Refreshs this project's attributes if, for example, the parent document's projects or tasks has been sorted*

        **Usage:**

            To refresh the project:

            .. code-block:: python

                myProject.refresh
        """

        if self.parent:
            self.parent.refresh
        title = self.title
        replace = self.parent.get_project(title)
        if not replace:
            return
        self.tags = replace.tags
        self.tasks = replace.tasks
        self.notes = replace.notes
        try:
            title = self.title
            replace = self.parent.get_project(title)
            self.tags = replace.tags
            self.tasks = replace.tasks
            self.notes = replace.notes
        except:
            pass
        self.projects = replace.projects
        try:
            self.projects = replace.projects
        except:
            pass

        self.content = replace.to_string(indentLevel=0, title=False)

        return

    def delete(
        self
    ):
        """*delete a project from the document*

        **Return:**
            - None

        **Usage:**

            .. code-block:: python

                myProject.delete()
        """

        projectTitle = self.title
        theseProjects = self.parent.projects[:]
        for p in theseProjects:
            if p.title == projectTitle:
                theseProjects.remove(p)
                break
        self.parent.projects = theseProjects

        doc = self
        while doc:
            if not doc.parent:
                break
            else:
                doc = doc.parent

        doc.content = doc.to_string(indentLevel=0, title=False)

        return None


class note(baseClass):
    """
    *The taskpaper note object*
    """

    def __repr__(self):
        return "<Note `%s`>" % self.title

    @property
    def projects(self):
        raise AttributeError("note object has no attribute 'projects'")

    @property
    def tasks(self):
        raise AttributeError("note object has no attribute 'tasks'")

    @property
    def notes(self):
        raise AttributeError("note object has no attribute 'notes'")

    def set_tags(self):
        raise AttributeError("note object has no 'set_tags' method")

    def add_tag(self):
        raise AttributeError("note object has no 'add_tag' method")

    def done(self):
        raise AttributeError("note object has no 'done' method")

    def get_project(self):
        raise AttributeError("note object has no 'get_project' method")

    def get_task(self):
        raise AttributeError("note object has no 'get_task' method")

    def tagged_projects(self):
        raise AttributeError("note object has no 'tagged_projects' method")

    def tagged_tasks(self):
        raise AttributeError("note object has no 'tagged_tasks' method")

    def sort_projects(self):
        raise AttributeError("note object has no 'sort_projects' method")

    def sort_tasks(self):
        raise AttributeError("note object has no 'sort_tasks' method")

    def add_project(self):
        raise AttributeError("note object has no 'add_project' method")

    def add_note(self):
        raise AttributeError("note object has no 'add_note' method")

    def add_task(self):
        raise AttributeError("note object has no 'add_task' method")
