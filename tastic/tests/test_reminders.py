import os
import nose
import shutil
import yaml
from tastic import reminders, cl_utils
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

pathToTaskpaperDoc = pathToOutputDir + "/tasks_imported_from_reminders.taskpaper"

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

# xt-setup-unit-testing-files-and-folders


class test_reminders():

    def test_reminders_function(self):

        from tastic import reminders
        this = reminders(
            log=log,
            settings=settings
        )
        this.import_list(
            listName="test list",
            pathToTaskpaperDoc=pathToTaskpaperDoc
        )

    def test_reminders_function_exception(self):

        from tastic import reminders
        try:
            this = reminders(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.import_list()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
