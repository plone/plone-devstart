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
import httplib
import urlparse
import urllib2
import subprocess
import zipfile

# Version of this script
devstart_version = "0.1"

# Base Python version and skeleton location for each base Plone version (to minor version)
plone_versions = {
    '4.1' : {
        'python_version': '2.6',
        'skeleton_url': 'https://github.com/optilude/plone-devstart/raw/master/closet/plone-4.1.zip',
    },
}
default_version = '4.1'

config = {
    'virtualenv_url': "https://raw.github.com/pypa/virtualenv/master/virtualenv.py",
    'bootstrap_url' : "http://python-distribute.org/bootstrap.py",
    'plone_kgs_url' : "http://dist.plone.org/release/%(plone_version)s/versions.cfg",
}

# Utilities

def download(url, directory, filename):
    """Download the given file into the given (or current) directory
    """

    # Thanks to http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
    u = urllib2.urlopen(url)
    f = open(os.path.join(directory, filename), 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "> Downloading: %s (%d bytes)" % (filename, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    print
    print "Done"
    f.close()

def run(command, *args):
    """Run the given command
    """
    print "> Running:", command, ' '.join(args)
    return subprocess.call([command] + list(args)) == 0

def ask(prompt, default=None):
    """Ask a question and return the response entered by the user
    """
    if default:
        prompt = prompt + " [%s] " % default
    answer = raw_input(prompt)
    if not answer and default:
        answer = default
    return answer

def check_url(url):
    """Check to see if the given URL exists
    """

    split = urlparse.urlsplit(url)
    connection = httplib.HTTPConnection(split.netloc, port=split.port)
    connection.request('HEAD', split.path)
    response = connection.getresponse()
    return response.status == 200

def get_base_version(version):
    """Turn a specific Plone or Python version into a base version
    """
    return '.'.join(version.split('.')[:2])

# Verification

def check_environment(version_config):
    """Given an intended Plone version, determine if the current Python version
    is acceptable
    """

    # TODO: Check for gcc if not on Windows

    python_version = version_config['python_version'].split('.')
    for i, e in enumerate(python_version):
        if i >= len(sys.version_info) or str(sys.version_info[i]) != e:
            return False
    return True

# Execution

def main():

    # TODO: Command line argument for version

    args = sys.argv
    directory =  os.getcwd()
    if len(args) > 1:
        directory = args[1]
    directory = os.path.abspath(directory)

    print
    print "Welcome to plone-devstart (version %s)" % devstart_version
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

    version = ask("Enter a Plone version number", default_version)
    base_version = get_base_version(version)

    while base_version not in plone_versions:
        print
        print "plone-devstart does not know what to do with this version."
        print "Known versions start with one of:", ", ".join(sorted(plone_versions.keys()))
        print "Please try again or press Ctrl+C to abort."
        print

        version = ask("Enter a Plone version number", default_version)
        base_version = get_base_version(version)

    version_config = plone_versions[base_version]

    kgs_url = config['plone_kgs_url'] % {'plone_version': version}
    print
    print "Checking for known good versions set at", kgs_url, "..."
    if not check_url(kgs_url):
        print
        print "** Warning: No known good set found at"
        print kgs_url
        print "Plone build will likely fail."
        print
        ask("Press Enter to continue, or Ctrl+C to abort")
    else:
        print "Done"

    if not check_environment(version_config):
        print
        print "** Warning: The current Python version is not known to work with Plone", version
        print "The expected Python version is", version_config['python_version'], "but this script is being run with Python"
        print "version", '.'.join([str(s) for s in sys.version_info])
        print "Plone build may fail."
        print
        ask("Press Enter to continue, or Ctrl+C to abort")

    print
    print "Creating build in directory", directory
    print
    create_directory(directory)

    print
    print "Creating virtual Python environment"
    print
    create_virtualenv(directory)

    print
    print "Obtaining skeleton buildout"
    print
    create_buildout(directory, version, version_config)

    print
    print "Bootstrapping buildout"
    print
    bootstrap(directory)

def create_directory(directory):
    """Create the build directory if necessary
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

def create_virtualenv(directory):
    """Create a virtualenv in the given directory
    """
    cwd = os.getcwd()

    download(config['virtualenv_url'], directory, 'virtualenv.py')

    os.chdir(directory)
    run(sys.executable, 'virtualenv.py', '--no-site-packages', directory)
    os.chdir(cwd)

def create_buildout(directory, plone_version, version_config):
    """Create a new buildout in the given directory
    """

    if os.path.exists(os.path.join(directory, 'buildout.cfg')):
        print
        print "** Warning: It looks like there is already a buildout.cfg file here."
        print "plone-devstart will not override it or recreate any other files"
        return

    # Download
    download(version_config['skeleton_url'], directory, 'buildout-skeleton.zip')

    # Unzip
    skeleton_file = os.path.join(directory, 'buildout-skeleton.zip')
    zf = zipfile.ZipFile(skeleton_file)

    for name in zf.namelist():
        f = zf.open(name)
        with open(os.path.join(directory, name), 'w') as f2:
            f2.write(f.read() % {
                'plone_kgs_url': config['plone_kgs_url'] % {'plone_version': plone_version},
            })
        f.close()

    # Delete the zip file
    os.unlink(skeleton_file)


def bootstrap(directory):
    """Bootstrap the buildout in the given directory
    """
    cwd = os.getcwd()
    download(config['bootstrap_url'], directory, 'bootstrap.py')

    os.chdir(directory)
    run(os.path.join(directory, 'bin', 'python'), 'bootstrap.py')
    os.chdir(cwd)

if __name__ == '__main__':
    main()
