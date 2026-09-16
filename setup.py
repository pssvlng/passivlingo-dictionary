""" Passivlingo Multilingual Dictionary
Copyright (C) Passivlingo (www.passivlingo.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """

import re
from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).parent

LONG_DESCRIPTION = HERE.joinpath('README.md').read_text(encoding='utf-8')

# Single source of truth for the version: read it from the package rather
# than duplicating it here, where the two would drift apart.
VERSION = re.search(
    r"^__version__ = ['\"]([^'\"]+)['\"]",
    HERE.joinpath('passivlingo_dictionary', '__init__.py').read_text(encoding='utf-8'),
    re.M,
).group(1)

setup(
    name='passivlingo_dictionary',
    packages=find_packages(exclude=['tests', 'tests.*']),
    version=VERSION,
    description=(
        'Unified multilingual WordNet access across the wn (OMW) and NLTK '
        'backends, with cross-lingual lookup and retrieval-step provenance'
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/pssvlng/passivlingo-dictionary',
    author='passivlingo',
    author_email='info@passivlingo.com',
    license='GPL 3',
    # Both core dependencies now require >=3.10 (nltk and wn). Supporting 3.9
    # would silently resolve older major versions of them — notably wn 0.x
    # rather than 1.x — which this package is not tested against.
    python_requires='>=3.10',
    # Runtime dependencies of the library itself. spaCy is included because
    # the tokenizer/lemmatizer factories import it at module load; textblob,
    # gtts, pyttsx3 and playsound back optional features and are extras.
    install_requires=[
        'wn>=0.9,<0.10',
        'nltk>=3.6',
        'spacy>=3.0',
    ],
    extras_require={
        # TextBlob-backed machine-translation provider.
        'translate': ['textblob>=0.15'],
        # Text-to-speech / audio helpers under Wrappers/.
        'audio': ['gtts', 'pyttsx3', 'playsound'],
        'test': ['pytest>=7'],
        'docs': ['sphinx>=7,<9', 'sphinx-rtd-theme>=2,<4'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    include_package_data=True,
)
