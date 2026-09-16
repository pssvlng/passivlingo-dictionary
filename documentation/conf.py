# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# Make the package importable without installing it, so autodoc can find it
# both locally and in the Read the Docs build environment.
sys.path.insert(0, os.path.abspath('..'))

import passivlingo_dictionary  # noqa: E402

# -- Project information -----------------------------------------------

project = 'passivlingo-dictionary'
copyright = '2026, Passivlingo'
author = 'Passivlingo'
version = passivlingo_dictionary.__version__
release = version

# -- General configuration -----------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest',
    'sphinx.ext.autosectionlabel',
]

# No custom templates or static assets yet. Both settings are intentionally
# empty: naming directories that do not exist makes Sphinx warn, which fails
# the documentation build under -W.
templates_path = []
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Autodoc: only document what modules declare in __all__, and preserve the
# order the code defines things in (not alphabetical) so related methods
# stay grouped the way the source groups them.
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': True,
}

# Google/NumPy-style docstring support (not currently used, but harmless to
# enable for contributors who prefer it over pure Sphinx-style).
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_rtype = False

# Cross-reference Python's own stdlib docs and the `wn` package's docs, so
# e.g. :class:`wn.Error` links out correctly from our compatibility notes.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'wn': ('https://wn.readthedocs.io/en/latest/', None),
}

# core.py's own docstrings reference Wordnet/Synset/Sense/Word/RelationCounts
# unqualified, since within that module they're in scope; doctest runs each
# docstring in a fresh namespace, so bring the same names into scope here.
doctest_global_setup = '''
import passivlingo_dictionary
from passivlingo_dictionary import (
    Wordnet, Word, Sense, Synset, RelationCounts, words, synsets, senses,
)
'''

# -- Options for HTML output -----------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = []
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 3,
}

# -- Autosection label options ---------------------------------------------

autosectionlabel_prefix_document = True
