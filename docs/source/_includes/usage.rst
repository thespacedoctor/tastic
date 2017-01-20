Command-Line Usage
==================

.. code-block:: bash 
   
    
    Documentation for tastic can be found here: http://tastic-for-taskpaper.readthedocs.io/en/stable/
    
    
    Usage:
        tastic init
        tastic sort <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
        tastic archive <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
        tastic [-f] sync <pathToWorkspace> <workspaceName> <pathToSyncFolder> [<editorialRootPath>] [-s <pathToSettingsFile>]
        tastic reminders import <listName> <pathToTaskpaperDoc> 
    
    Options:
        init                     setup the tastic settings file for the first time
        sort                     sort a taskpaper file or directory containing taskpaper files via workflow tags in settings file
        archive                  move done tasks in the 'Archive' projects within taskpaper documents into markdown tasklog files
        reminders                commands to work with macOS reminders
        import                   import tasks into a given taskpaper document
    
    
        pathToFileOrWorkspace    give a path to an individual taskpaper file or the root of a workspace containing taskpaper files
        pathToTaskpaperDoc       a path to a taskpaper document
        pathToWorkspace          root path of a workspace containing taskpaper files
        workspaceName            the name you give to the workspace
        pathToSyncFolder         path to the folder you wish to sync the index task files into
        listName                 name of a reminders.app list (macOS only)
        editorialRootPath        the root path of editorial's dropbox sync folder (add to generate an editorial URL for each task)
        -h, --help               show this help message
        -v, --version            show version
        -s, --settings           the settings file
        -f, --fileTags           if the tag to sync is in the filepath (e.g. /@due/mytasks.taskpaper) include all items the file in that tag set
    
    
