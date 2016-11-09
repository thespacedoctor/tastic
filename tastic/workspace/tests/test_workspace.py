import os
import nose
import shutil
import yaml
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

# # load settings
# stream = file(
#     "/Users/Dave/.config/tastic/tastic.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()

import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

workspaceRoot = pathToOutputDir + "/astronotes-wiki"


class test_workspace():

    def test_workspace_function(self):

        from tastic.workspace import workspace
        ws = workspace(
            log=log,
            settings=settings,
            fileOrWorkspacePath=workspaceRoot
        )
        ws.sort()
        ws.archive_done()

    def test_workspace_function02(self):

        from tastic.workspace import workspace
        ws = workspace(
            log=log,
            settings=settings,
            fileOrWorkspacePath=pathToOutputDir +
            "/astronotes-wiki/projects/@due/PESSTO-ESO-SSDR3/PESSTO-ESO-SSDR3.taskpaper"
        )
        ws.sort()

    def test_workspace_archive_function01(self):

        from tastic.workspace import workspace
        ws = workspace(
            log=log,
            settings=settings,
            fileOrWorkspacePath=pathToOutputDir +
            "/astronotes-wiki/projects/@due/PESSTO-ESO-SSDR3/PESSTO-ESO-SSDR3.taskpaper"
        )
        ws.archive_done()

    def test_workspace_function_exception(self):

        from tastic.workspace import workspace
        try:
            this = workspace(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.sort()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
