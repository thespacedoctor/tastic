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


class test_tastic():

    def test_doc_function(self):

        # READ IN A TASKPAPER FILE
        from tastic.tastic import document
        taskpaperFile = pathToOutputDir + "/saturday-tasks.taskpaper"
        doc = document(taskpaperFile)

        # TIDY THE DOCUMENT
        doc.tidy()

        # SAVE A DUPLICATE OF THE DOC
        doc.save(pathToOutputDir + "/saturday-tasks-copy.taskpaper")

        # ADD SAVE THE ORIGINAL
        doc.save(pathToOutputDir + "/saturday-tasks.taskpaper")

        # LIST THE PROJECT IN THE DOC
        docProjects = doc.projects
        for p in docProjects:
            continue
            print p.title

        # FILTER PROJECTS
        dueProjects = doc.tagged_projects("@due")
        for p in dueProjects:
            continue
            print p.title

        # GET A PROJECT BY NAME
        gardenProject = doc.get_project("tidy the garden")

        # SORT PROJECTS
        doc.sort_projects("@due, @flag, @hold, @next, @someday, @wait")
        doc.save()

        # gardenProject.refresh

        # ADD A NEW PROJECT
        shedProject = gardenProject.add_project(
            title="build a shed",
            tags="@someday @garden"
        )
        gardenProject.refresh

        researchShedProject = shedProject.add_project(
            title="research shed designs",
            tags="@research"
        )

        coffee = doc.get_project("make coffee").done()

        doc.get_project("replace hedge with fence").delete()

        docTasks = doc.tasks
        for t in docTasks:
            continue
            print t.title

        hotTasks = doc.tagged_tasks("@hot")
        for t in hotTasks:
            continue
            print t.title

        doc.sort_tasks("@due, @flag, @hold, @next, @someday, @wait")
        doc.save()

        coffee.refresh
        for t in coffee.tasks:
            t.done("all")

        print ""
        aTask = researchShedProject.add_task(
            "look for 5 videos on youtube", "@online")

        bTask = aTask.add_task("note the urls of the most useful videos")

        # NOTES
        doc.get_project("grocery shop").notestr()

        newNote = doc.add_note(
            "make sure to make time to do nothing")

        # print aTask.tasks
        newNote = aTask.add_note(
            "good video: https://www.youtube.com/watch?v=nMaGTP82DtI")

        aTask.add_tag("@due")
        # print aTask.to_string()

        researchShedProject.add_tag("@hold")
        # print researchShedProject.to_string()

        aTask.set_tags("@someday")
        # print aTask.to_string()

        researchShedProject.set_tags("@someday")
        # print researchShedProject.to_string()

        aTask.set_tags()
        # print aTask.to_string()

        doc.save()
        # print
        # print aTask.to_string()

        # aTask = doc.add_task(
        #     "bite me", "@online")
