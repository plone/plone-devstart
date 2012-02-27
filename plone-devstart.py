"""Create a "safe" Plone development environment starting from nothing but
Python.

Usage::

    $ python plone-devstart <dirname>

If directory name is omitted, the current directory is used.

This will:

* Download ``virtualenv.py`` and ``bootstrap.py``
* Run it with the current interpreter to create an isolated development
  environment
* Create and bootstrap a new buildout for Plone using this interpreter

You will be asked several questions along the way:

* Plone version to use. This should be within the range of versions known to
  this version of ``plone-devstart``, otherwise you will be given an warning.
* A choice of whether to create a skeleton package for your custom code.
  If you choose this option, some additional questions will be asked:

  * Package name (which will be normalised)
  * Whether or not to create a skeleton Diazo theme
  * Whether or not to enable content types
"""

import sys

# Base Python version for each base Plone version (to minor version)
python_versions = {
    '4.0': '2.6',
    '4.1': '2.6',
    '4.2': '2.6',
}

config = dict(
    virtualenv_url = "https://raw.github.com/pypa/virtualenv/master/virtualenv.py",
    bootstrap_url = "http://python-distribute.org/bootstrap.py",
    plone_kgs_url = "http://dist.plone.org/release/%(plone_version)s/versions.cfg",
)

templates = dict(

    buildout_cfg = """\
[buildout]
parts =
    instance
    test
    coverage-report
    zopepy
    zopeskel
    checkversions
    mkrelease
#    omelette

extends =
    packages.cfg

# Packages to check out/update when buildout is run
auto-checkout =
    %(package_name)s

# Make sure buildout always attempts to update packages
always-checkout = force

# Development Zope instance. Installs the ``bin/instance`` script
[instance]
recipe = plone.recipe.zope2instance
http-address = 8080
user = admin:admin
verbose-security = on
eggs =
    ${eggs:main}
    ${eggs:devtools}

# Test runner. Run: ``bin/test`` to execute all tests
[test]
recipe = zc.recipe.testrunner
eggs = ${eggs:test}
defaults = ['--auto-color', '--auto-progress']

# Coverage report generator.
# Run: ``bin/test --coverage=coverage``
# and then: ``bin/coveragereport``
[coverage-report]
recipe = zc.recipe.egg
eggs = z3c.coverage
scripts = coveragereport
arguments = ('parts/test/coverage', 'coverage')

# Installs the ``bin/zopepy`` interpreter.
[zopepy]
recipe = zc.recipe.egg
eggs =
    ${eggs:main}
    ${eggs:devtools}
interpreter = zopepy

# Installs ZopeSkel, which can be used to create new packages
# Run: ``bin/zopeskel``
[zopeskel]
recipe = zc.recipe.egg
eggs = ZopeSkel

# Tool to help check for new versions.
# Run: ``bin/checkversions versions.cfg``
[checkversions]
recipe = zc.recipe.egg
eggs = z3c.checkversions [buildout]

# Tool to make releases
# Run: ``bin/mkrelease --help``
[mkrelease]
recipe = zc.recipe.egg
eggs = jarn.mkrelease

# Installs links to all installed packages to ``parts/omelette``.
# On Windows, you need to install junction.exe first
[omelette]
recipe = collective.recipe.omelette
eggs =
    ${eggs:main}
    ${eggs:devtools}
""",

    packages_cfg = """\
[buildout]
extensions = mr.developer buildout.dumppickedversions
extends =
# Known good sets of eggs we may be using
    %(plone_kgs_url)s
    versions.cfg

versions = versions
unzip = true

# Egg sets
[eggs]
main =
    Plone
test =
devtools =
    plone.reload
    Products.PDBDebugMode
    Products.PrintingMailHost
    Products.DocFinderTab

# Checkout locations
[sources]
%(package_checkout)s
""",

    versions_cfg = """\
[versions]
# Buildout
mr.developer = 1.20
collective.recipe.omelette = 0.12

# Development tools
Products.DocFinderTab = 1.0.4
Products.PDBDebugMode = 1.3.1
Products.PrintingMailHost = 0.7
z3c.coverage = 1.2.0
jarn.mkrelease = 3.5
setuptools-git = 0.4.2
setuptools-hg = 0.4

# ZopeSkel
ZopeSkel = 3.0a1
Cheetah = 2.4.4
Paste = 1.7.5.1
PasteScript = 1.7.5
PasteDeploy = 1.5.0
""",

)

# Utilities

def download(url, directory):
    """Download the given file into the directory
    """

def run(command):
    """Run the given command
    """

def ask(prompt, default):
    """Ask a question and return the response entered by the user
    """

def check_url(url):
    """Check to see if the given URL exists
    """

# Verification

def check_python_version(plone_version):
    """Given an intended Plone version, determine if the current Python version
    is acceptable
    """

# Execution

def main():
    """
    """

def create_virtualenv(directory):
    """Create a virtualenv in the given directory
    """

def create_buildout(directory, data):
    """Create a new buildout in the given directory
    """

def bootstrap(directory):
    """Bootstrap the buildout in the given directory
    """

if __name__ == '__main__':
    main()
