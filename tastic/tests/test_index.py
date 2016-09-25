import os
import nose
import shutil
import yaml
from tastic import index
from tastic.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="tastic",
    tunnel=False
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

try:
    shutil.rmtree(pathToOutputDir + "/home")
except:
    pass
try:
    shutil.rmtree(pathToOutputDir + "/work")
except:
    pass


shutil.copytree(pathToInputDir + "/home", pathToOutputDir + "/home")
shutil.copytree(pathToInputDir + "/work", pathToOutputDir + "/work")


class test_index():

    def test_index_function(self):

        from tastic import index
        this = index(
            log=log,
            settings=settings
        )

    def test_index_function_exception(self):

        from tastic import index
        try:
            this = index(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
