Development buildout
=====================

This buildout has been generated using ``plone-devstart``. It consists of the
following top-level files:

* ``buildout.cfg``, which will build a single Zope instance with a number of
  development tools.
* ``deployment.cfg``, which will build four Zope instances and a ZEO database
  server for them all to connect to.
* ``packages.cfg``, which they both extend, and which lists out packages making
  up the build, including Plone.
* ``versions.cfg``, which is extended by ``packages.cfg``, and which pins down
  package versions for a few of the tools not included in the standard Plone
  Known Good Setup.

Running the build
-----------------

The build should already have been bootstrapped by ``plone-devstart``. If not,
run::

    $ bin/python bootstrap.py

This assumes an appropriate virtual environment has been created in the buildout
directory, as is done by ``plone-devstart``. If not, use an appropriate Python
interpereter above.

With the build bootstrapped, run the development buildout with::

    $ bin/buildout

Use the ``--help`` option for more options.

To start up Zope and access Plone, run::

    $ bin/instance fg

Development tools
-----------------

The development build installs a number of tools, outlined below.

``lxml``
    If you are on Mac OS X, you should install a static version of ``lxml``.
    This is left commented out by default, so uncomment the ``lxml`` line at
    the top of ``buildout.cfg`` if you want this.
Test runner
    Packages listed in the ``test`` list under ``[eggs]`` in ``packages.cfg``
    can be run with the test runner that is installed as ``bin/test``.
Coverage reporting
    Run ``bin/test --coverage=coverage`` and then ``bin/coveragereport`` to
    generate a detailed test statement coverage report in the ``coverage/``
    directory.
``zopepy``
    A basic interpreter with all the packages required by Zope available can be
    run using ``bin/zopepy``.
ZopeSkel
    To generate new packages from skeletons, run ``bin/zopeskel`` and follow
    the instructions. You should probably run this from within the ``src/``
    directory, since that is where you will likely want packages to live,
    in which case the command becomes ``../bin/zopeskel``.
``checkversions``
    Use the ``bin/checkversions`` script to check for newer versions of packages
    you have pinned in ``versions.cfg``.
``jarn.mkrelease``
    If you create new packages and plan to release them to PyPI or a custom
    egg server, you can use the ``bin/mkrelease`` script.
Omelette
    To generate a symbolically linked, single source tree of all the Python
    packages in the Zope build, uncomment the ``omelette`` line near the
    top of ``buildout.cfg``. On Windows, you will need ``junction.exe``
    installed and some degree of patience, which is why it is commented out by
    default. The files can be useful for grepping and inspection, and are found
    in ``parts/omelette`` after Buildout has run.
``plone.reload``
    If you make Python code changes whilst Zope is running in debug mode
    (e.g. when started with ``bin/instance fg``), you can reload the changed
    code by going to ``http://localhost:8080/@@reload``.
``Products.PDBDebugMode``
    This product ensures that a PDB debugging session is started whenever an
    uncaught exception is raised. Beware that this can cause Zope to appear to
    hang, until you press ``c`` followed by ``Enter`` in the console where
    Zope is running.
``Products.PrintingMailHost``
    This product causes mail sent from Zope to be printed to the console when
    Zope is running in debug mode, instead of sending it via SMTP.
``Products.DocFinderTab``
    Adds a ``Doc`` tab in the ZMI, providing a way to discover methods and
    documentation on objects.
``plone.app.debugtoolbar``
    Provides a wealth of contextual debugging tools and information in a
    pull-down toolbar inside Plone. For this to be enabled, you must install
    the *Debug toolbar* profile from Plone's *Add-ons* control panel.

Customisations package
----------------------

By default, this buildout provides a Python distribution in the ``src/`` called
``plone-customizations``. It consists of a single top-level package called
``customizations``, which provides:

* A GenericSetup profile
* A custom browser layer
* A ``z3c.jbot`` template overrides directory
* Skeletal integration tests based on ``plone.app.testing``

The idea is that you can put simple project-specific customisation in this
package. In theory, you can also create content types and other components here
as well.

See the ``README.txt`` file in ``src/plone-customizations`` for more details.

The layout of this distribution is deliberably simplified compared to usual
Plone conventions. You should *not* release this package to PyPI, and it may
well conflict with an equivalent package in other project based on
``plone-devstart``. However, project-specific customisations tend to also be
build-specific, so that may not matter.

The ``plone-customizations`` distribution is enabled as a "develop egg" using
the ``mr.developer`` Buildout extension. In ``packages.cfg``, we have::

    [sources]
    plone-customizations = fs plone-customizations

Furthermore, in ``buildout.cfg`` and ``deployment.cfg`` we have::

    auto-checkout =
        plone-customizations

These lines tell Buildout where to find the development distribution (on the
filesystem, inside the ``src/`` directory), and inform ``mr.developer`` to
enable it each time the build is run.

If you want to create more granular packages, you can use ZopeSkel, found in
``bin/zopeskel`` when the development build is run. You would then list these
in the ``[sources]`` block. You can independenlty version control such packages,
to allow them to have a deployment lifecycle that is independent of the buildout
in which they are used. See the
`mr.developer documentation <http://pypi.python.org/pypi/mr.developer>`_ for
more details.

Deployment
----------

To run the deployment buildout, which is somewhat optimised for production use
and does not include any testing or development tools, run::

    $ bin/buildout -c deployment.cfg

This will build four Zope instances and one ZEO database server. Host names,
port numbers and user accounts can all be set in the ``deployment.cfg`` file.

The Zope instances can be started manually with::

    $ bin/zeo start
    $ bin/instance1 start
    $ bin/instance2 start
    $ bin/instance3 start
    $ bin/instance4 console

Use ``stop`` instead of ``start`` to stop the daemonised processes.

On Linux or Mac OS X, you can use Supervisor to manage the processes. To
install it, uncomment the ``supervisor`` line near the top of ``deployment.cfg``
before running the build. You can then start the Supervisor daemon with::

    $ bin/supervisord

This will start all the relevant processes. You can then manage them on
``http://localhost:9001``, or using the ``bin/supervisorctl`` script.

In all cases, this build will provide a way to run multiple load-balanced Zope
instances, as is recommended for performant deployments. (You generally want
one Zope instance per CPU core, each with 1 or 2 threads). However, you will
need some way to load balance between them. Common options for doing so include:

* A web cache such as Varnish, which also boosts performance by acting as
  caching proxy.
* A web server such as nginx or Apache.
* A dedicated load balancer such as HAProxy or Pound.

You can learn more about hosting in the book *Professional Plone 4 Development*
or at http://collective-docs.readthedocs.org/en/latest/hosting/index.html.
