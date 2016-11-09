import os
import nose
import shutil
import yaml
from tastic.tastic import document
from tastic.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="tastic"
)
arguments, settings, log, dbConn = su.setup()


# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/tastic.yaml", 'r')
settings = yaml.load(stream)
stream.close()

shutil.copyfile(pathToInputDir + "/saturday-tasks.taskpaper",
                pathToOutputDir + "/saturday-tasks.taskpaper")

shutil.copyfile(pathToInputDir + "/ssdr3.taskpaper",
                pathToOutputDir + "/ssdr3.taskpaper")


class test_tastic():

    # def test_doc_function(self):

    #     # READ IN A TASKPAPER FILE
    #     from tastic.tastic import document
    #     taskpaperFile = pathToOutputDir + "/saturday-tasks.taskpaper"
    #     doc = document(taskpaperFile)

    #     # DISPLAY THE RAW CONTENT OF THE DOCUMENT
    #     print doc.raw_content

    #     # DOCUMENT PROJECTS
    #     docProjects = doc.projects
    #     firstProject = docProjects[0]

    #     # TASK PAPER PROJECT ATTRIBUTES
    #     print firstProject.raw_content
    #     print firstProject.content
    #     print firstProject.title
    #     print firstProject.parent
    #     print "\n\n"

    #     # DOCUMENT NOTES
    #     print "NOTES:"
    #     docNotes = doc.notes
    #     for n in docNotes:
    #         print n.title
    #     print "\n\n"

    #     # GET A PROJECT
    #     archiveProject = doc.get_project("Archive")
    #     print archiveProject.title
    #     print archiveProject.to_string()
    #     print "\n\n"

    #     print "FILTER PROJECTS BY TAG"
    #     filteredProjects = doc.tagged_projects("flag")
    #     for p in filteredProjects:
    #         print p.title

    #     print "FILTER TASK BY TAG"
    #     filteredTasks = doc.tagged_tasks("@flag")
    #     for t in filteredTasks:
    #         print t.title

    #     print "SORT PROJECTS"
    #     doc.sort_projects("@due, @flag, @hold, @next, @someday, @wait")

    #     print "SORT TASKS"
    #     doc.sort_tasks("@due, @flag, @hold, @next, @someday, @wait")

    #     print "TIDY DOCUMENT"
    #     doc.tidy()

    #     print "ADD PROJECT"
    #     doc.add_project("this is a project I added", "@with @tags")
    #     doc.add_project("this is a second project I added", "@with @tags")

    #     for p in docProjects:
    #         p.add_project(
    #             ">>>>>>>>>>>>>>>> this is a subproject I added", "@with @tags")
    #         p.add_project(">>>>>>>>>>>>>>>> and another added subproject:",
    #                       ['@with', '@tags(data)'])

    #     print "ADD TASKS"
    #     doc.add_task("this is a task I added", "@with @tags")
    #     doc.add_task("and another added task",
    #                  ['@with', '@tags(data)'])

    #     print "ADD NOTE"
    #     doc.add_note("""Nullam dignissim vulputate nulla vel fermentum. Praesent in nibh efficitur, accumsan tellus at, tincidunt quam. Curabitur enim leo, condimentum eget bibendum ac, suscipit id tortor. Proin sed placerat mauris. Pellentesque in eleifend massa. Fusce tincidunt eget risus at scelerisque. Mauris vel rutrum arcu, sit amet tempus nibh. Praesent volutpat elit sed felis luctus, a accumsan nisl convallis. Nullam eros ex, malesuada eget turpis sodales, sollicitudin tempus est. Vivamus odio augue, ornare non imperdiet eleifend, gravida id velit. Phasellus a congue felis. Morbi pharetra sit amet nulla id mattis. Sed sagittis, ex maximus pellentesque suscipit, mi diam fringilla tortor, eu faucibus lorem lorem et odio. Donec blandit nec quam sit amet facilisis. Sed nec sodales nulla, in pretium libero. Fusce tempus lorem vel ligula euismod tincidunt.""")
    #     doc.add_note(
    #         """And another note with a link http://www.thespacedoctor.co.uk""")

    #     print doc.content

    #     # # DOCUMENT SEARCHES
    #     docSearches = doc.searches
    #     print docSearches

    #     # DOCUMENT TASKS
    #     print "TASKS:"
    #     docTasks = doc.tasks
    #     print docTasks
    #     print "\n\n"

    #     print "\n\n"

    #     print "GET PROJECT"
    #     archiveProject = doc.get_project("Archive")
    #     if archiveProject:
    #         print archiveProject.to_string()
    #     print "\n\n"

    #     return

    def test_doc2_function(self):

        # READ IN A TASKPAPER FILE
        from tastic.tastic import document
        taskpaperFile = pathToOutputDir + "/ssdr3.taskpaper"
        doc = document(taskpaperFile)

        # DISPLAY THE RAW CONTENT OF THE DOCUMENT
        # print doc.raw_content

        # DOCUMENT PROJECTS
        docProjects = doc.projects

        firstProject = docProjects[0]

        # TASK PAPER PROJECT ATTRIBUTES
        # print firstProject.raw_content
        # print firstProject.content
        # print firstProject.title
        # print firstProject.parent
        # print "\n\n"

        # DOCUMENT NOTES
        # print "NOTES:"
        docNotes = doc.notes
        # for n in docNotes:
        #     print n.title
        # print "\n\n"

        # GET A PROJECT
        archiveProject = doc.get_project("Archive")
        # print archiveProject.title
        # print archiveProject.to_string()
        # print "\n\n"

        # print "FILTER PROJECTS BY TAG"
        filteredProjects = doc.tagged_projects("flag")
        # for p in filteredProjects:
        #     print p.title

        # print "FILTER TASK BY TAG"
        filteredTasks = doc.tagged_tasks("@flag")
        # for t in filteredTasks:
        #     print t.title

        print "TIDY DOCUMENT"
        # doc.tidy()

        # print "SORT PROJECTS"
        doc.sort_projects("@due, @flag, @hold, @next, @someday, @wait")

        # print "SORT TASKS"
        doc.sort_tasks("@due, @flag, @hold, @next, @someday, @wait")

        # print "ADD PROJECT"
        # doc.add_project("this is a project I added", "@with @tags")
        # doc.add_project("this is a second project I added", "@with @tags")

        # for p in docProjects:
        #     p.add_project(
        #         ">>>>>>>>>>>>>>>> this is a subproject I added", "@with @tags")
        #     p.add_project(">>>>>>>>>>>>>>>> and another added subproject:",
        #                   ['@with', '@tags(data)'])

        # print "ADD TASKS"
        # doc.add_task("this is a task I added", "@with @tags")
        # doc.add_task("and another added task",
        #              ['@with', '@tags(data)'])

        # print "ADD NOTE"
        # doc.add_note("""Nullam dignissim vulputate nulla vel fermentum. Praesent in nibh efficitur, accumsan tellus at, tincidunt quam. Curabitur enim leo, condimentum eget bibendum ac, suscipit id tortor. Proin sed placerat mauris. Pellentesque in eleifend massa. Fusce tincidunt eget risus at scelerisque. Mauris vel rutrum arcu, sit amet tempus nibh. Praesent volutpat elit sed felis luctus, a accumsan nisl convallis. Nullam eros ex, malesuada eget turpis sodales, sollicitudin tempus est. Vivamus odio augue, ornare non imperdiet eleifend, gravida id velit. Phasellus a congue felis. Morbi pharetra sit amet nulla id mattis. Sed sagittis, ex maximus pellentesque suscipit, mi diam fringilla tortor, eu faucibus lorem lorem et odio. Donec blandit nec quam sit amet facilisis. Sed nec sodales nulla, in pretium libero. Fusce tempus lorem vel ligula euismod tincidunt.""")
        # doc.add_note(
        #     """And another note with a link http://www.thespacedoctor.co.uk""")

        # # # DOCUMENT SEARCHES
        # docSearches = doc.searches
        # print docSearches

        # # DOCUMENT TASKS
        # print "TASKS:"
        # docTasks = doc.tasks
        # print docTasks
        # print "\n\n"

        # print "\n\n"

        # print "GET PROJECT"
        # archiveProject = doc.get_project("Archive")
        # if archiveProject:
        #     print archiveProject.to_string()
        # print "\n\n"

        doc.save()

        print doc.to_string()

        return

    # def test_projects_function(self):

    #     # DOCUMENT LEVEL METHODS AND PROPERTIES
    #     # LOAD UP THE TASKPAPER FILE
    #     taskpaperFile = pathToOutputDir + "/saturday-tasks.taskpaper"
    #     doc = document(taskpaperFile)

    #     # PROJECT LEVEL METHODS AND PROPERTIES
    #     # GET ALL THE PROJECT OBJECTS WITHIN THE DOCUMENT
    #     docProjects = doc.projects

    #     for p in docProjects:

    #         # PROJECT TITLE
    #         print "TITLE:"
    #         pTitle = p.title
    #         print pTitle
    #         print "\n\n"

    #         # PROJECT RAW CONTENT
    #         print "RAW CONTENT:"
    #         pRaw = p.raw_content
    #         print pRaw
    #         print "\n\n"

    #         # PROJECT CONTENT
    #         print "CONTENT:"
    #         pContent = p.content
    #         print pContent
    #         print "\n\n"

    #         # PROJECT PROJECTS
    #         print "SUBPROJECTS:"
    #         subProjects = p.projects
    #         print subProjects
    #         print "\n\n"

    #         # PROJECT TASKS
    #         print "TASKS:"
    #         pTasks = p.tasks
    #         print pTasks
    #         print "\n\n"

    #         # PROJECT NOTES
    #         print "NOTES:"
    #         pNotes = p.notes
    #         print pNotes
    #         print "\n\n"

    #         p.add_project(
    #             "this is a subproject I added", "@with @tags")
    #         p.add_project("and another added subproject:",
    #                       ['@with', '@tags(data)'])

    #         p.add_note("""Nullam id odio est. Vivamus eget nibh diam. Phasellus laoreet vel purus et pellentesque. Etiam condimentum, purus vitae finibus dignissim, metus felis aliquet leo, in bibendum lectus urna vel lectus. Nullam quis nunc vitae dolor posuere finibus sed in ex. Vestibulum eleifend imperdiet pretium. In in finibus nisi. Curabitur quis orci odio. Nullam ultrices interdum nibh, eget lacinia sapien vestibulum at. Nunc consequat posuere lectus, in scelerisque arcu ornare nec.""")

    #         print "ADD TASKS"
    #         p.add_task("this is a task I added to a subproject", "@with @tags")
    #         p.add_task("and another added task added to a subproject",
    #                    ['@with', '@tags(data)'])
    #         print "\n\n"

    #         # PROJECT TAGS
    #         print "TAGS:"
    #         pTags = p.tags
    #         print pTags
    #         print "\n\n"

    #     print "TIDY DOCUMENT"
    #     doc.tidy()
    #     print doc.content
    #     print "\n\n"

    #     return

    # def test_task_function(self):

    #     # DOCUMENT LEVEL METHODS AND PROPERTIES
    #     # LOAD UP THE TASKPAPER FILE
    #     taskpaperFile = pathToOutputDir + "/saturday-tasks.taskpaper"
    #     doc = document(taskpaperFile)

    #     # TASK LEVEL METHODS AND PROPERTIES
    #     # GET ALL THE ROOT TASK OBJECTS WITHIN THE DOCUMENT
    #     docTasks = doc.tasks

    #     for t in docTasks:

    #         # TASK TITLE
    #         print "TITLE:"
    #         tTitle = t.title
    #         print tTitle
    #         print "\n\n"

    #         # TASK RAW CONTENT
    #         print "RAW CONTENT:"
    #         tRaw = t.raw_content
    #         print tRaw
    #         print "\n\n"

    #         # TASK CONTENT
    #         print "CONTENT:"
    #         tContent = t.content
    #         print tContent
    #         print "\n\n"

    #         # TASK TASKS
    #         print "TASKS:"
    #         tTasks = t.tasks
    #         print tTasks
    #         print "\n\n"

    #         # TASK NOTES
    #         print "NOTES:"
    #         tNotes = t.notes
    #         print tNotes
    #         print "\n\n"

    #         # TASK TAGS
    #         print "TAGS:"
    #         tTags = t.tags
    #         print tTags
    #         print "\n\n"

    #     return
