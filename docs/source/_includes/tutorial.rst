Command-Line Tools Tutorial
===========================

As well as providing python objects and methods for working with your taskpaper documents, tastic also provides some very useful command-line tools. These tools work not only with single taskpaper documents, but also with entire workspaces (nested folders) containing taskpaper documents.

Before you begin using the tastic command-line tools you will need to populate some custom settings within your tastic settings file.

To setup the default settings file at ``~/.config/tastic/tastic.yaml`` run the command:

.. code-block:: bash 
    
    tastic init

This should create and open the settings file; follow the instructions in the file to populate the missing settings values (usually given an ``XXX`` placeholder). 

Sorting Taskpaper Docs via Workflow Tags
----------------------------------------

For details about exactly what happens when you sort a taskpaper document's projects and tasks via workflow tags, see the `sorting projects by tags`_ and `sorting tasks by tags`_ sections of the python code tutorial. But for now let's see how to achieve sorting via the command-line.

In the settings file you will find a set of workflow tags, which you can adapt to your liking:

.. code-block:: yaml 
    
    worflowTags: "@due, @flag, @hold, @next, @someday, @wait"

To sort an individual taskpaper document's projects and tasks via these workflow tags (ordered from most to least prioritised) use the command:

.. code-block:: bash

    tastic sort /path/to/my/doc.taskpaper

If you want to sort the taskpaper documents recursively contained within a workspace, pass instead the root-path of the workspace:

.. code-block:: bash

    tastic sort /path/to/my/workspace/

Moving Archived `@done` Tasks to a Markdown Log File
--------------------------------------------------

To move completed tasks found in the *Archive* project of a taskpaper document into an adjacent markdown file run the command:

.. code-block:: bash

    tastic archive /path/to/my/doc.taskpaper

This moves the completed archived tasks into a markdown file located at `/path/to/my/doc-tasklog.md` and formats them into a neat, complete-date ordered table (completed date only added if `@done` tags includes the completion date as an attribute, e.g. `@done(2016-11-09)`).

Again if you want to run this code on all taskpaper documents contained within a workspace, pass instead the root-path of the workspace:

.. code-block:: bash

    tastic archive /path/to/my/workspace/

Python Code Tutorial
====================

Before we start, you'll need an example taskpaper document to work with. Copy and paste the following example document content into a taskpaper file somewhere on your file system:

.. code-block:: text 
    
    - invite friends over for drinks


    make coffee: @coffee @flag
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - wait for 3 minutes @wait
        - plunge the coffee in the cafetiere 
        - pour into cup @hot
        - drink
            ahhhhhhh that's good

    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.

    - do get hair cut @due

    tidy the garden: @flag
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass


        replace hedge with fence: @due
            - watch a couple of youtube videos about putting up a fence @flag
            buy fence materials:
            the hedge at the rear of the garden
            - ask neighbours if I can work from their garden to fix the fence

    this is a rolling document where I can add projects and task I know I can only get done on saturdays

    - take the boys to the cinema if it's raining @someday

    grocery shop: @due
        - carrots
        - shampoo
        - beer
        - washing detergent
        The super-market closes at 8pm on saturdays

    - take the boys to the park @next

    - put up shelves in living room @flag

    Archive:
        - research the price of fencing online @done(2016-09-15) @project(tidy the garden / replace hedge with fence)
        - clear the garden @done(2016-09-15) @project(tidy the garden / cut the grass)
        


    [Searches]: @hide
        - do: due @search(/project @due//* union //@due and not @done)
        - do: flag @search(/project @flag//* union //@flag and not @done)
        - do: projects to tag @search(/project not "@" and not "archive"//*)
        - review: next or someday @search(project @next or @someday//* )
        - Project List @search(/project not @someday)
        - Next and Someday List @search(/project @next or @someday)
 
Taskpaper Objects
-----------------

If you're unfamiliar with the `taskpaper <https://www.taskpaper.com/>`_ syntax, head over to `Jesse Grosjean's User Guide for Taskpaper 3 <https://guide.taskpaper.com/>`_.

There are 5 basic components to the taskpaper syntax that tastic recognises; these are:

1. documents
2. projects
3. tasks
4. notes
5. tags
   
Working with documents
----------------------

I'm going to assume that you've saved the example file above to your desktop and named the file *saturday-tasks.taskpaper*. Fire up ipython and let's get stuck in.

Reading a document
~~~~~~~~~~~~~~~~~~

To read the file into memory use the following python code:

.. code-block:: python 
    
    from tastic.tastic import document
    doc = document("/Users/<yourusername>/Desktop/saturday-tasks.taskpaper") 

This command reads the content of the file and automatically tidies it for you. To view the content of the file run the following:

.. code-block:: python 

    print doc.content

And as you can see we now have a nice clean, ordered document; notes first, then tasks, then projects, then searches:

.. code-block:: plain

    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays
    - invite friends over for drinks
    - do get hair cut @due
    - take the boys to the cinema if it's raining @someday
    - take the boys to the park @next
    - put up shelves in living room @flag
    make coffee: @coffee @flag
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - wait for 3 minutes @wait
        - plunge the coffee in the cafetiere
        - pour into cup @hot
        - drink
            ahhhhhhh that's good
    tidy the garden: @flag
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass
        replace hedge with fence: @due
            the hedge at the rear of the garden
            - watch a couple of youtube videos about putting up a fence @flag
            - ask neighbours if I can work from their garden to fix the fence
            buy fence materials:
    grocery shop: @due
        The super-market closes at 8pm on saturdays
        - carrots
        - shampoo
        - beer
        - washing detergent
    Archive:
        - research the price of fencing online @done(2016-09-15) @project(tidy the garden / replace hedge with fence)
        - clear the garden @done(2016-09-15) @project(tidy the garden / cut the grass)
    [Searches]: @hide
        - do: due @search(/project @due//* union //@due and not @done)
        - do: flag @search(/project @flag//* union //@flag and not @done)
        - do: projects to tag @search(/project not "@" and not "archive"//*)
        - review: next or someday @search(project @next or @someday//* )
        - Project List @search(/project not @someday)
        - Next and Someday List @search(/project @next or @someday) 

If at any stage in your code you want to tidy the document again (not that you should need to), run the command:

.. code-block:: python 
    
    doc.tidy() 

Writing a document
~~~~~~~~~~~~~~~~~~

Note any changes you make to the content of the document will have to be saved back to the file. To save the document at any stage run the command:

.. code-block:: python 

    doc.save()

or to save the content to a different file:

.. code-block:: python 

    doc.save("/Users/<yourusername>/Desktop/saturday-tasks-copy.taskpaper")

Note, if you save the content to another file, any further edits to the content of the file will be saved to this new location with `save()`.

Working with projects
---------------------

Both documents and projects themselves can contain sub-projects.

Get a project by name
~~~~~~~~~~~~~~~~~~~~~

To select out a single project by it's title use the `get_project` method:

.. code-block:: python 
    
    gardenProject = doc.get_project("tidy the garden")
    print gardenProject.to_string()

 .. code-block:: text

    tidy the garden: @flag
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass
        replace hedge with fence: @due
            the hedge at the rear of the garden
            - watch a couple of youtube videos about putting up a fence @flag
            - ask neighbours if I can work from their garden to fix the fence
            buy fence materials:

Also note the use of the `to_string()` method. This method can be used on documents, projects, tasks and notes to convert the object to a string.

Lising projects
~~~~~~~~~~~~~~~

To compile a list of root-level projects within your document, use the `projects` attribute:

.. code-block:: python 

    docProjects = doc.projects
        for p in docProjects:
            print p.title

.. code-block:: text

    make coffee:
    tidy the garden:
    grocery shop:
    Archive: 

All projects also have a `projects` attribute so you can drill down into a document's project tree to work with any sub-project. For example:

.. code-block:: python 

    subProjects = gardenProject.projects
    for p in subProjects:
        print p.title

.. code-block:: text

    build bbq:
    cut the grass:
    replace hedge with fence:

Filtering projects by tag
~~~~~~~~~~~~~~~~~~~~~~~~~

To filter projects by an associated tag, use the `tagged_projects` method:

.. code-block:: python 
    
    dueProjects = doc.tagged_projects("@due")
    for p in dueProjects:
        print p.title 

.. code-block:: text

    replace hedge with fence:
    grocery shop: 

The keen eyed among you will notice that this filter is in fact recursive, picking up all projects within the document with the "@due" tag and not just the root level projects. Again each project has a `tagged_projects` method to allow for finer grain filtering of projects.

Sorting projects by tags
~~~~~~~~~~~~~~~~~~~~~~~~

`sort_projects` is one of my favorite methods. Given a list of workflow tags, you can sort projects recursively within a taskpaper document or project. In the example below projects tagged with `@due` rise to the top of their parent object, followed by `@flag` projects and so on. Projects not associated with any of the workflow tags are sorted after matched projects.

.. code-block:: python 

    doc.sort_projects("@due, @flag, @hold, @next, @someday, @wait")
    doc.save()
    print doc.content()

.. code-block:: text

    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays
    - invite friends over for drinks
    - do get hair cut @due
    - take the boys to the cinema if it's raining @someday
    - take the boys to the park @next
    - put up shelves in living room @flag
    grocery shop: @due
        The super-market closes at 8pm on saturdays
        - carrots
        - shampoo
        - beer
        - washing detergent
    make coffee: @coffee @flag
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - wait for 3 minutes @wait
        - plunge the coffee in the cafetiere 
        - pour into cup @hot
        - drink
            ahhhhhhh that's good
    tidy the garden: @flag
        replace hedge with fence: @due
            the hedge at the rear of the garden
            - watch a couple of youtube videos about putting up a fence @flag
            - ask neighbours if I can work from their garden to fix the fence
            buy fence materials:
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass
    Archive:
        - research the price of fencing online @done(2016-09-15) @project(tidy the garden / replace hedge with fence)
        - clear the garden @done(2016-09-15) @project(tidy the garden / cut the grass)
    [Searches]: @hide
        - do: due @search(/project @due//* union //@due and not @done)
        - do: flag @search(/project @flag//* union //@flag and not @done)
        - do: projects to tag @search(/project not "@" and not "archive"//*)
        - review: next or someday @search(project @next or @someday//* )
        - Project List @search(/project not @someday)
        - Next and Someday List @search(/project @next or @someday)

Marking a project as done
~~~~~~~~~~~~~~~~~~~~~~~~~

To mark a project as done, use the `done()` method:

.. code-block:: python 

    coffee = doc.get_project("make coffee").done()
    print coffee.to_string()

.. code-block:: text

    make coffee: @done(2016-09-17 21:49:49)
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - wait for 3 minutes @wait
        - plunge the coffee in the cafetiere 
        - pour into cup @hot
        - drink
            ahhhhhhh that's good

It's also possible to mark all descendant items of the object as `@done` by using `.done("all")`.

Adding a project
~~~~~~~~~~~~~~~~

After sorting all the projects in the document you may have to use the `refresh` attribute for any project you have in the local namespace to refresh its attributes.

.. code-block:: python 
    
    gardenProject.refresh

Now to add a sub-project use the `add_project` method (this also works on the document object):

.. code-block:: python 

    # ADD A NEW PROJECT
    shedProject = gardenProject.add_project(
        title="build a shed",
        tags="@someday @garden"
    )

    researchShedProject = shedProject.add_project(
        title="research shed designs",
        tags="@research"
    )

    print doc.content

.. code-block:: text

    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays
    - invite friends over for drinks
    - do get hair cut @due
    - take the boys to the cinema if it's raining @someday
    - take the boys to the park @next
    - put up shelves in living room @flag
    grocery shop: @due
        The super-market closes at 8pm on saturdays
        - carrots
        - shampoo
        - beer
        - washing detergent
    make coffee: @coffee @flag
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - wait for 3 minutes @wait
        - plunge the coffee in the cafetiere 
        - pour into cup @hot
        - drink
            ahhhhhhh that's good
    tidy the garden: @flag
        replace hedge with fence: @due
            the hedge at the rear of the garden
            - watch a couple of youtube videos about putting up a fence @flag
            - ask neighbours if I can work from their garden to fix the fence
            buy fence materials:
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass
        build a shed: @someday @garden
            research shed designs: @research
    Archive:
        - research the price of fencing online @done(2016-09-15) @project(tidy the garden / replace hedge with fence)
        - clear the garden @done(2016-09-15) @project(tidy the garden / cut the grass)
    [Searches]: @hide
        - do: due @search(/project @due//* union //@due and not @done)
        - do: flag @search(/project @flag//* union //@flag and not @done)
        - do: projects to tag @search(/project not "@" and not "archive"//*)
        - review: next or someday @search(project @next or @someday//* )
        - Project List @search(/project not @someday)
        - Next and Someday List @search(/project @next or @someday)

Deleting a project
~~~~~~~~~~~~~~~~~~

To delete a project, use the `delete()` method

.. code-block:: python 

    doc.get_project("replace hedge with fence").delete()
    print doc.content

.. code-block:: text

    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays
    - invite friends over for drinks
    - do get hair cut @due
    - take the boys to the cinema if it's raining @someday
    - take the boys to the park @next
    - put up shelves in living room @flag
    grocery shop: @due
        The super-market closes at 8pm on saturdays
        - carrots
        - shampoo
        - beer
        - washing detergent
    make coffee: @done(2016-09-19 10:02:58)
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - wait for 3 minutes @wait
        - plunge the coffee in the cafetiere 
        - pour into cup @hot
        - drink
            ahhhhhhh that's good
    tidy the garden: @flag
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass
        build a shed: @someday @garden
            research shed designs: @research
    Archive:
        - research the price of fencing online @done(2016-09-15) @project(tidy the garden / replace hedge with fence)
        - clear the garden @done(2016-09-15) @project(tidy the garden / cut the grass)
    [Searches]: @hide
        - do: due @search(/project @due//* union //@due and not @done)
        - do: flag @search(/project @flag//* union //@flag and not @done)
        - do: projects to tag @search(/project not "@" and not "archive"//*)
        - review: next or someday @search(project @next or @someday//* )
        - Project List @search(/project not @someday)
        - Next and Someday List @search(/project @next or @someday)


Working with tasks
------------------

Listing Tasks
~~~~~~~~~~~~~

Documents, projects and tasks can all contain tasks. To get a list of the  objects tasks, use its `tasks` attribute.

.. code-block:: python 
    
    docTasks = doc.tasks
    for t in docTasks:
        print t.title 

.. code-block:: text 
    
    - invite friends over for drinks
    - do get hair cut
    - take the boys to the cinema if it's raining
    - take the boys to the park
    - put up shelves in living room

Filtering Tasks by tags
~~~~~~~~~~~~~~~~~~~~~~~

To filter tasks by an associated tag, use the `tagged_tasks` method:

.. code-block:: python 
    
    hotTasks = doc.tagged_tasks("@hot")
    for t in hotTasks:
        print t.title

.. code-block:: text

    - fill cafetiere with boiled water from kettle
    - pour into cup

As with the project filter, the task filter is recursive, picking up all tasks within the document with the "@hot" tag and not just the root level tasks. Again each project and task has a `tagged_tasks` method to allow for finer grain filtering of tasks.

Sorting tasks by tags
~~~~~~~~~~~~~~~~~~~~~

Given a list of workflow tags, you can sort tasks recursively within a taskpaper document, project or task. In the example below tasks tagged with `@due` rise to the top of their parent object, followed by `@flag` task and so on. Tasks not associated with any of the workflow tags are sorted after matched tasks.

.. code-block:: python 
    
    doc.sort_tasks("@due, @flag, @hold, @next, @someday, @wait")
    doc.save()
    print doc.content

.. code-block:: text 
    
    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays
    - do get hair cut @due
    - put up shelves in living room @flag
    - take the boys to the park @next
    - take the boys to the cinema if it's raining @someday
    - invite friends over for drinks
    grocery shop: @due
        The super-market closes at 8pm on saturdays
        - carrots
        - shampoo
        - beer
        - washing detergent
    make coffee: @done(2016-09-19 13:27:19)
        - wait for 3 minutes @wait
        - scoop 3 heaped tablespoons of coffee into cafetiere
        - fill cafetiere with boiled water from kettle @hot @water
        - plunge the coffee in the cafetiere 
        - pour into cup @hot
        - drink
            ahhhhhhh that's good
    tidy the garden: @flag
        build bbq: @someday
        cut the grass:
            - has it stopped raining yet @hold
                you can check the weather here: http://forecast.io/
            - get the mower out
            - put welly boots on
            - cut the grass
        build a shed: @someday @garden
            research shed designs: @research
    Archive:
        - research the price of fencing online @done(2016-09-15) @project(tidy the garden / replace hedge with fence)
        - clear the garden @done(2016-09-15) @project(tidy the garden / cut the grass)
    [Searches]: @hide
        - do: due @search(/project @due//* union //@due and not @done)
        - do: flag @search(/project @flag//* union //@flag and not @done)
        - do: projects to tag @search(/project not "@" and not "archive"//*)
        - review: next or someday @search(project @next or @someday//* )
        - Project List @search(/project not @someday)
        - Next and Someday List @search(/project @next or @someday) 

    
Marking a task as done
~~~~~~~~~~~~~~~~~~~~~~

To mark a task as done, use the `done()` method:

.. code-block:: python 

    coffee.refresh
    for t in coffee.tasks:
        t.done("all")

    print coffee.to_string()

.. code-block:: text

    make coffee: @done(2016-09-19 16:05:50)
        - wait for 3 minutes @done(2016-09-19 16:05:50)
        - scoop 3 heaped tablespoons of coffee into cafetiere @done(2016-09-19 16:05:50)
        - fill cafetiere with boiled water from kettle @done(2016-09-19 16:05:50)
        - plunge the coffee in the cafetiere @done(2016-09-19 16:05:50)
        - pour into cup @done(2016-09-19 16:05:50)
        - drink @done(2016-09-19 16:05:50)
            ahhhhhhh that's good
        
Adding a task
~~~~~~~~~~~~~

A task can be added to a document, project or task object using the `add_task` method:

.. code-block:: python 

    aTask = researchShedProject.add_task("look for 5 videos on youtube", "@online")
    aTask.add_task("note the urls of the most useful videos")
    print researchShedProject.to_string()

.. code-block:: text 

    research shed designs: @research
        - look for 5 videos on youtube @online
            - note the urls of the most useful videos

Working with notes
------------------

Documents, project and tasks can all have notes assigned to them.

Listing notes
~~~~~~~~~~~~~

To list the notes for any given object use the `notestr()` method. 

.. code-block:: python 

    doc.notestr()

.. code-block:: text 

    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays

.. code-block:: python 
    
    print doc.get_project("grocery shop").notestr()

.. code-block:: text 
    
    The super-market closes at 8pm on saturdays 


Adding a note
~~~~~~~~~~~~~

Use the `add_note()` method to add notes to documents, projects and tasks:

.. code-block:: python 
    
    newNote = doc.add_note("make sure to make time to do nothing")
    print doc.notestr() 

.. code-block:: text 
    
    I need to review this document every month or so to add new tasks and project, refresh and tidy current projects and clear out stale ones.
    this is a rolling document where I can add projects and task I know I can only get done on saturdays
    make sure to make time to do nothing 

.. code-block:: python 

    newNote = aTask.add_note(
        "good video: https://www.youtube.com/watch?v=nMaGTP82DtI")
    print aTask.to_string()

.. code-block:: text 

    - look for 5 videos on youtube @online
        good video: https://www.youtube.com/watch?v=nMaGTP82DtI
        - note the urls of the most useful videos

Working with tags
-----------------

Adding a tag to a project or task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add (append) a tag to a task or project use the `add_tag` method.

.. code-block:: python 

    aTask.add_tag("@due")
    print aTask.to_string()

.. code-block:: text 

    - look for 5 videos on youtube @online @due
        good video: https://www.youtube.com/watch?v=nMaGTP82DtI
        - note the urls of the most useful videos

.. code-block:: python 

    researchShedProject.add_tag("@hold")
    print researchShedProject.to_string()

.. code-block:: text 

    research shed designs: @research @hold
        - look for 5 videos on youtube @online @due
            good video: https://www.youtube.com/watch?v=nMaGTP82DtI
            - note the urls of the most useful videos

Setting a project's or task's tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of adding a tag, you can replace all of the tags using the `set_tags()` method.

.. code-block:: python 

    researchShedProject.set_tags("@someday")
    print researchShedProject.to_string()

.. code-block:: text 

    research shed designs: @someday
        - look for 5 videos on youtube @someday
            good video: https://www.youtube.com/watch?v=nMaGTP82DtI
            - note the urls of the most useful videos

.. code-block:: python 

    researchShedProject.set_tags("@someday")
    print researchShedProject.to_string()

.. code-block:: text 

    research shed designs: @someday
        - look for 5 videos on youtube @someday
            good video: https://www.youtube.com/watch?v=nMaGTP82DtI
            - note the urls of the most useful videos

Removing all tags from a project or task
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To delete all of the tags, use the `set_tags()` method with no argument:

.. code-block:: python 

    researchShedProject.set_tags()
    print researchShedProject.to_string()

.. code-block:: text 

    - look for 5 videos on youtube
        good video: https://www.youtube.com/watch?v=nMaGTP82DtI
        - note the urls of the most useful videos

