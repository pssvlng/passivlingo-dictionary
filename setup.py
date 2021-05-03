from setuptools import find_packages, setup

setup(
    name='passivlingo_dictionary',
    packages=find_packages(),            
    version='0.1.0',
    description='Python package for accessing OWN and NLTK wordnet ontologies',    
    url='https://github.com/pssvlng/passivlingo-dictionary',
    author='passivlingo',
    author_email='info@passivlingo.com',
    license='GPL 3',
    install_requires=['wn==0.6.2', 'nltk', 'spacy', 'textblob'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Software Development :: NLP Package',
        'Programming Language :: Python :: 3',
    ]
)    

        


