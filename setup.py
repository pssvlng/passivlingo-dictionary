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

from setuptools import find_packages, setup

setup(
    name='passivlingo_dictionary',
    packages=find_packages(),            
    version='1.0.1',
    description='Python package for accessing OWN and NLTK wordnet ontologies',    
    url='https://github.com/pssvlng/passivlingo-dictionary',
    author='passivlingo',
    author_email='info@passivlingo.com',
    license='GPL 3',
    install_requires=['wn', 'nltk', 'spacy', 'textblob', 'pyttsx3', 'gtts', 'playsound'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True
)    

        


