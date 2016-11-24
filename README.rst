tastic 
=========================

*A python package for working with taskpaper documents*.

Here's a summary of what's included in the python package:

.. include:: /classes_and_functions.rst

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
    
    

Documentation
=============

Documentation for tastic is hosted by `Read the Docs <http://tastic-for-taskpaper.readthedocs.io/en/stable/>`__ (last `stable version <http://tastic-for-taskpaper.readthedocs.io/en/stable/>`__ and `latest version <http://tastic-for-taskpaper.readthedocs.io/en/latest/>`__).

Installation
============

The easiest way to install tastic us to use ``pip``:

.. code:: bash

    pip install tastic

Or you can clone the `github repo <https://github.com/thespacedoctor/tastic>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/tastic.git
    cd tastic
    python setup.py install

To upgrade to the latest version of tastic use the command:

.. code:: bash

    pip install tastic --upgrade


Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

.. code:: bash

    git clone git@github.com:thespacedoctor/tastic.git
    cd tastic
    python setup.py develop

`Pull requests <https://github.com/thespacedoctor/tastic/pulls>`__
are welcomed!

Sublime Snippets
~~~~~~~~~~~~~~~~

If you use `Sublime Text <https://www.sublimetext.com/>`_ as your code editor, and you're planning to develop your own python code with tastic, you might find `my Sublime Snippets <https://github.com/thespacedoctor/tastic-Sublime-Snippets>`_ useful. 

Issues
------

Please report any issues
`here <https://github.com/thespacedoctor/tastic/issues>`__.

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

