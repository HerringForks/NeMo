# ! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2020 NVIDIA. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""Setup for pip package."""

import codecs
import os
import subprocess
import sys
from distutils import cmd as distutils_cmd
from distutils import log as distutils_log
from itertools import chain

import setuptools


def is_build_action():
    if len(sys.argv) <= 1:
        return False

    BUILD_TOKENS = ["egg_info", "dist", "bdist", "sdist", "install", "build", "develop"]

    if any([sys.argv[1].startswith(x) for x in BUILD_TOKENS]):
        return True
    else:
        return False


if is_build_action():
    os.environ['NEMO_PACKAGE_BUILDING'] = 'True'

from nemo.package_info import (
    __contact_emails__,
    __contact_names__,
    __description__,
    __download_url__,
    __homepage__,
    __keywords__,
    __license__,
    __package_name__,
    __repository_url__,
    __version__,
)

if os.path.exists('README.rst'):
    # codec is used for consistent encoding
    long_description = codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'), 'r', 'utf-8',
    ).read()
    long_description_content_type = "text/x-rst"

elif os.path.exists('README.md'):
    with open("README.md", "r") as fh:
        long_description = fh.read()
    long_description_content_type = "text/markdown"

else:
    long_description = 'See ' + __homepage__


###############################################################################
#                             Dependency Loading                              #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


def req_file(filename, folder="requirements"):
    with open(os.path.join(folder, filename)) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters
    # Example: `\n` at the end of each line
    return [x.strip() for x in content]


install_requires = req_file("requirements.txt")

extras_require = {
    # User packages
    'docker': req_file("requirements_docker.txt"),
    'test': req_file("requirements_test.txt"),
    # Collections Packages
    'asr': req_file("requirements_asr.txt"),
    'nlp': req_file("requirements_nlp.txt"),
    'simple_gan': req_file("requirements_simple_gan.txt"),
    'tts': req_file("requirements_tts.txt"),
}

extras_require['all'] = list(chain(extras_require.values()))

# TTS depends on ASR
extras_require['tts'] = list(chain([extras_require['tts'], extras_require['asr']]))

tests_requirements = extras_require["test"]


###############################################################################
#                            Code style checkers                              #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


class StyleCommand(distutils_cmd.Command):
    __LINE_WIDTH = 119
    __ISORT_BASE = (
        'isort '
        # These two lines makes isort compatible with black.
        '--multi-line=3 --trailing-comma --force-grid-wrap=0 '
        f'--use-parentheses --line-width={__LINE_WIDTH} -rc'
    )
    __BLACK_BASE = f'black --skip-string-normalization --line-length={__LINE_WIDTH}'
    description = 'Checks overall project code style.'
    user_options = [
        ('scope=', None, 'Folder of file to operate within.'),
        ('fix', None, 'True if tries to fix issues in-place.'),
    ]

    def __call_checker(self, base_command, scope, check):
        command = list(base_command)

        command.append(scope)

        if check:
            command.extend(['--check', '--diff'])

        self.announce(
            msg='Running command: %s' % str(' '.join(command)), level=distutils_log.INFO,
        )

        return_code = subprocess.call(command)

        return return_code

    def _isort(self, scope, check):
        return self.__call_checker(base_command=self.__ISORT_BASE.split(), scope=scope, check=check,)

    def _black(self, scope, check):
        return self.__call_checker(base_command=self.__BLACK_BASE.split(), scope=scope, check=check,)

    def _pass(self):
        self.announce(msg='\033[32mPASS\x1b[0m', level=distutils_log.INFO)

    def _fail(self):
        self.announce(msg='\033[31mFAIL\x1b[0m', level=distutils_log.INFO)

    # noinspection PyAttributeOutsideInit
    def initialize_options(self):
        self.scope = '.'
        self.fix = ''

    def run(self):
        scope, check = self.scope, not self.fix
        isort_return = self._isort(scope=scope, check=check)
        black_return = self._black(scope=scope, check=check)

        if isort_return == 0 and black_return == 0:
            self._pass()
        else:
            self._fail()
            exit(isort_return if isort_return != 0 else black_return)

    def finalize_options(self):
        pass


###############################################################################


setuptools.setup(
    name=__package_name__,
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,
    description=__description__,
    long_description=long_description,
    # The project's main homepage.
    url=__repository_url__,
    download_url=__download_url__,
    # Author details
    author=__contact_names__,
    author_email=__contact_emails__,
    # maintainer Details
    maintainer=__contact_names__,
    maintainer_email=__contact_emails__,
    # The licence under which the project is released
    license=__license__,
    classifiers=[
        # How mature is this project? Common values are
        #  1 - Planning
        #  2 - Pre-Alpha
        #  3 - Alpha
        #  4 - Beta
        #  5 - Production/Stable
        #  6 - Mature
        #  7 - Inactive
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        # Indicate what your project relates to
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',
        # Supported python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # Additional Setting
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_requirements,
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # $ pip install -e ".[all]"
    # $ pip install nemo_toolkit[all]
    extras_require=extras_require,
    # Add in any packaged data.
    include_package_data=True,
    zip_safe=False,
    # PyPI package information.
    keywords=__keywords__,
    # Custom commands.
    cmdclass={'style': StyleCommand},
)