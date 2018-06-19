# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os

import django
from sphinx.application import Sphinx


# -- Project information -----------------------------------------------------

project = 'CRATE'
copyright = '2018, Rudolf Cardinal'
author = 'Rudolf Cardinal'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx.ext.autodoc',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# See http://www.sphinx-doc.org/en/master/theming.html
# html_theme = 'alabaster'  # elegant but monochrome
html_theme = 'classic'  # like the Python docs. GOOD. CHOSEN.
# html_theme = 'sphinxdoc'  # OK; TOC on right
# html_theme = 'scrolls'  # ugly
# html_theme = 'agogo'  # nice, but a bit big-print; TOC on right; justified
# html_theme = 'traditional'  # moderately ugly
# html_theme = 'nature'  # very nice. Used for CamCOPS.
# html_theme = 'haiku'  # dosen't do sidebar
# html_theme = 'pyramid'  # Once inline code customized, GOOD.
# html_theme = 'bizstyle'  # OK

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# https://stackoverflow.com/questions/18969093/how-to-include-the-toctree-in-the-sidebar-of-each-page
html_sidebars = {
    '**': ['globaltoc.html', 'relations.html', 'sourcelink.html',
           'searchbox.html']
}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'CRATEdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'CRATE.tex', 'CRATE Documentation',
     'Rudolf Cardinal', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'crate', 'CRATE Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'CRATE', 'CRATE Documentation',
     author, 'CRATE', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -----------------------------------------------------------------------------
# RNC: add CSS
# -----------------------------------------------------------------------------
# https://stackoverflow.com/questions/23462494/how-to-add-a-custom-css-file-to-sphinx

def setup(app: Sphinx) -> None:
    app.add_stylesheet('css/crate_docs.css')  # may also be an URL


# -----------------------------------------------------------------------------
# RNC: autodoc
# -----------------------------------------------------------------------------
# http://www.sphinx-doc.org/en/stable/ext/autodoc.html#confval-autodoc_mock_imports  # noqa
# https://stackoverflow.com/questions/36228537/django-settings-module-not-defined-when-building-sphinx-documentation

autodoc_mock_imports = [
    "servicemanager",  # Windows only
    "win32event",  # Windows only
    "win32service",  # Windows only
    "win32serviceutil",  # Windows only
    "winerror",  # Windows only
]

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# sys.path.insert(0, os.path.join(os.path.abspath('.'), '../../myproj'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'crate_anon.crateweb.config.settings'
django.setup()
