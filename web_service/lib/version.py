"""
Return a version string from the _version.py file.
Right now, this version is manually incremented. One potential
improvement would be to generate this version from git or such.
"""
import re
from flask import current_app
import os


def version_string():
    version_file = os.path.join(current_app.root_path, '_version.py')
    version_line = open(version_file, 'r').read()

    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    match = re.search(version_re, version_line, re.M)

    if match:
        return match.group(1)
    else:
        raise RuntimeError('Unable to parse version string from file {}'.format(version_file))
