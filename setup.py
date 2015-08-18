""":mod:docutils` setup.py file to generate Python compatible sources in
build/ directory
"""
import os
import glob
import fnmatch
import shutil
from setuptools import setup

VERSION = '0.0.0'


def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


def find_data_files(srcdir, *wildcards, **kw):
    """Get a list of all files under the *srcdir* matching *wildcards*,
    returned in a format to be used for install_data.

    """
    def walk_helper(arg, dirname, files):
        names = []
        lst, wildcards = arg
        for wildcard in wildcards:
            wc_name = opj(dirname, wildcard)
            for current_file in files:
                filename = opj(dirname, current_file)

                if (fnmatch.fnmatch(filename, wc_name) and
                        not os.path.isdir(filename)):
                    if kw.get('version') is None:
                        names.append(filename)
                    else:
                        versioned_file = '%s.%s' % (filename,
                                                    kw.get('version'))
                        shutil.copyfile(filename, versioned_file)
                        names.append('%s.%s' % (filename,
                                                kw.get('version')))

        if names:
            if kw.get('target_dir') is None:
                lst.append(('', names))
            else:
                lst.append((kw.get('target_dir'), names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(current_file) for current_file in glob.glob(opj(srcdir, '*'))])

    return file_list

# find_data_files('trols_munger_ui/conf/',
#                 '*.conf',
#                 version=VERSION)

# find_data_files('trols_munger_ui/templates/')

setup(name='python-trols-munger-ui',
      version=VERSION,
      description='TROLS-Munger-UI',
      author='Lou Markovski',
      author_email='lou.markovski@gmail.com',
      url='',
      packages=['trols_munger_ui',
                'trols_munger_ui.views'],
      include_package_data=True)
