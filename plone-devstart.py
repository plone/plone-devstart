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

You will be asked several questions along the way
"""

import os
import os.path
import sys

# Base Python version and skeleton location for each base Plone version (to minor version)
plone_versions = {
    '4.1' : {
        'python': '2.6',
        'skeleton': 'https://raw.github.com/optilude/plone-devstart/closet/plone-4.1.zip',
    },
}
default_version = '4.1'

config = {
    'virtualenv_url': "https://raw.github.com/pypa/virtualenv/master/virtualenv.py",
    'bootstrap_url' : "http://python-distribute.org/bootstrap.py",
    'plone_kgs_url' : "http://dist.plone.org/release/%(plone_version)s/versions.cfg",
}

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

def get_base_version(version):
    """Turn a specific Plone or Python version into a base version
    """

# Verification

def check_python_version(plone_version):
    """Given an intended Plone version, determine if the current Python version
    is acceptable
    """

# Execution

def main():

    args = sys.argv
    directory =  os.getcwd()
    if len(args) > 1:
        directory = args[1]

    print
    print "Welcome to plone-devstart."
    print "Press Ctrl+C any time to abort"
    print

    print "Please enter the Plone version you would like to start with."
    print "Version numbers can be found at http://dist.plone.org/release"
    print
    print "plone-devstart knows about the following base versions:"
    print
    print "  ", ", ".join(sorted(plone_versions.keys()))
    print
    print "You can use a more specific revision of any of these, e.g. 4.1.2"
    print

    version = raw_input("Enter a Plone version number [%s] " % default_version)
    base_version = get_base_version(version)

    while base_version not in plone_versions:
        print "plone-devstart does not know what to do with this version."
        print "Known versions start with one of: ", ", ".join(sorted(plone_versions.keys()))
        print "Please try again or press Ctrl+C to abort."
        print

        version = raw_input("Enter a Plone version number [%s] " % default_version)
        base_version = get_base_version(version)

    kgs_url = config['plone_kgs_url'] % version
    if not check_url(kgs_url):
        print "Warning: No known good set found at", kgs_url
        print "Plone build will likely fail."
        print
        input("Press Enter to continue, or Ctrl+C to abort")

    if not check_python_version(version):
        print "Warning: The current Python version is not known to work with Plone ", version

        python_version = plone_versions.get(base_version, {}).get('python_version', None)
        if python_version is not None:
            print "The expected Python version is ", python_version        

        print "Plone build may fail."
        print
        input("Press Enter to continue, or Ctrl+C to abort")


def create_directory(directory):
    """Ensure the given directory exists
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
