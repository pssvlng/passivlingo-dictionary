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
    version='0.0.2',
    description='Python package for accessing OWN and NLTK wordnet ontologies',    
    url='https://github.com/pssvlng/passivlingo-dictionary',
    author='passivlingo',
    author_email='info@passivlingo.com',
    license='GPL 3',
    install_requires=['wn==0.6.2', 'nltk==3.6.2', 'spacy==3.0.6', 'textblob==0.15.3', 'pyttsx3==2.90', 'gtts==2.2.2', 'playsound==1.2.2'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True
)    

        


