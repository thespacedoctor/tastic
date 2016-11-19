Command-Line Usage
==================

.. code-block:: bash 
   
    
    Documentation for tastic can be found here: http://tastic-for-taskpaper.readthedocs.io/en/stable/
    
    
    Usage:
        tastic init
        tastic sort <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
        tastic archive <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
        tastic sync <pathToWorkspace> <workspaceName> <pathToSyncFolder> [-s <pathToSettingsFile>]
    
    Options:
        init                     setup the tastic settings file for the first time
        sort                     sort a taskpaper file or directory containing taskpaper files via workflow tags in settings file
        archive                  move done tasks in the 'Archive' projects within taskpaper documents into markdown tasklog files
    
        pathToFileOrWorkspace    give a path to an individual taskpaper file or the root of a workspace containing taskpaper files
        pathToWorkspace          root path of a workspace containing taskpaper files
        workspaceName            the name you give to the workspace
        pathToSyncFolder         path to the folder you wish to sync the index task files into
        -h, --help               show this help message
        -v, --version            show version
        -s, --settings           the settings file
    
    
