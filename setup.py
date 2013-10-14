import os
from distutils.core import setup
from setuptools import find_packages
from version import VERSION

VERSION = VERSION

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Documentation',
    'Topic :: Software Development',
    'Topic :: Text Processing :: Markup'
]

INSTALL_REQUIRES = [
    "Pygments>=1.6",
    "Sphinx>=1.1.3",
    "docutils>=0.11"
]

setup(
    name = "rst2code",
    description = "reStructuredText literate programming tool",
    classifiers = CLASSIFIERS,
    install_requires = INSTALL_REQUIRES,
    version = VERSION,
    author = "Jean-Matthieu BARBIER",
    author_email = "jm.barbier@solidev.net",
    url="https://github.com/jmbarbier/rst2code",
    download_url="https://github.com/jmbarbier/rst2code/archive/v"+VERSION+".tar.gz",
    py_modules = ["rst2code"]
)
