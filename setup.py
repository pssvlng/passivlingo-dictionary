from setuptools import find_packages, setup

setup(
    name='passivlingo_dictionary',
    packages=find_packages(),            
    version='0.1.0',
    description='Python library for accessing OWN and NLTK wordnet ontologies',
    author='passivlingo',
    author_email='info@passivlingo.com',
    license='GPL 3',
    install_requires=['wn==0.6.2', 'nltk', 'spacy', 'textblob'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)    

        


