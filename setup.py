from setuptools import find_packages, setup

setup(
    name='passivlingo_dictionary',
    packages=find_packages(),            
    version='0.0.1',
    description='Python package for accessing OWN and NLTK wordnet ontologies',    
    url='https://github.com/pssvlng/passivlingo-dictionary',
    author='passivlingo',
    author_email='info@passivlingo.com',
    license='GPL 3',
    install_requires=['wn', 'nltk', 'spacy', 'textblob', 'pyttsx3'],
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

        


