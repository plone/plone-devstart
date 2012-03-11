plone-devstart
==============

``plone-devstart.py`` is a script to quickly and safely bootstrap a useful Plone
development environment.

All you need is the single script, ``plone-devstart.py``::

    $ curl -O https://raw.github.com/plone/plone-devstart/master/plone-devstart.py

You run it with::

    $ python plone-devstart.py <directory>

This will create a Plone development environment in the given directory.

**Note**: If no directory is specified, the build will be created in the
current directory.

**Important:** You must run ``plone-devstart.py`` with a version of Python
that is compatible with the intended Plone version. You will be warned if this
is not the case.

To view other options, see::

    $ python plone-devstart.py --help

When ``plone-devstart`` is run, it will:

* Ask for a Plone version number. This must be within a known major/minor
  version compbination, e.g. a version in the 4.1 series such as 4.1.4.
  To skip this manual entry step, use the ``--version`` command line option.
* Check that a Known Good Set of packages exists for this version of Plone.
* Check that the version of Python used to run ``plone-devstart.py`` is
  compatible with the target version of Plone.
* If on a non-Windows platform: check for a C compiler (``cc``), Python
  header files, and ``libjpeg`` header files (necessary for the Python
  Imaging Library).
* Check for ``zlib`` and SSL support in Python.
* Create the target directory, if it does not exist.
* Download ``virtualenv.py`` and create an isolated virtual Python environment
  in this directory. This has the effect of creating a Python interpreter that
  is unaware of any glolbally installed "site packages" that may interfere
  with Plone's own versions of certain packages.
* Download a skeleton Buildout for this version of Plone (see below). If the
  file ``buildout.cfg`` exists, this step will be skipped, unless the
  ``--force`` command line option is given.
* Download ``bootstrap.py`` and bootstrap the Buildout environment with the
  isolated virtual environment Python interpreter.

Buildout
--------

The Buildout created by ``plone-devstart.py`` contains various development
tools, and a simple distribution (in the ``src/`` directory) called
``plone-customizations`` that can be used to house template overrides,
configuration or other customisations to Plone.

The buildout, which may vary between Plone versions, will contain a
``README.txt`` file with details of how it is configured and used.

Version control
---------------

If you wish to put the build under version control, you should ignore the
following files (e.g. in a ``.gitignore`` file if using Git  or as the
``svn:ignore`` property in Subversion)::

    *.pyc
    .installed.cfg
    .mr.developer.cfg
    .DS_Store
    Thumbs.db
    bin
    eggs
    develop-eggs
    include
    lib
    parts
    var

Recreating an environment
-------------------------

If you have obtained an environment from source control or elsewhere, and want
to perform the ``plone-devstart.py`` system checks and create an isolated
Python environment, you can run ``python plone-devstart.py`` (with an
appropriate version of Python and possibly with a relative or absolute path
to the ``plone-devstart.py`` script) from within an existing directory.

So long as you do not use the ``--force`` option, this will perform all of the
steps above except downloading and extracting the skeleton build. This should
leave all your custom files intact, but will create a new, isolated Python
environment and bootstrap buildout to use this.

Frequently Asked Questions
--------------------------

* Should I not just use the Plone Universal or Windows installers?

Possibly, yes. The installers provide a better-tested, fully standalone
environment. If you are mostly interested in getting Plone up and running,
they are the best place to start. See `<http://plone.org/download>`_.

``plone-devstart`` is, as its name implies, more geared at development and
customisation. It is able to work with arbitrary versions of Plone, and
is lighter weight in that it doesn't install its own Python binary. It also
provides a buildout setup with some development tools and a place to put basic
customisations.

The key point here is that ``plone-devstart`` assumes you have an appropriate
Python version installed already. It will check version compatibility, but
otherwise it allows you to use a system-installed or custom compiled Python.

* Why not use ``ZopeSkel`` or ``Paste Script`` to build this?

The advantage of ``plone-devstart`` is that it is a single script with no
dependencies. There is no need to hava a functioning ``easy_install`` or ``pip``
to be able to use it.
