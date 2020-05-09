# -*- coding: utf-8 -*-

import os, sys, time
from urllib.parse import quote
# get current directory and cut off the '/docs' so sphinx can find the source code
sys.path.append(os.getcwd()[:-5])

print(sys.path)

import warnings

warnings.filterwarnings("ignore", category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                                ' non-GUI backend, so cannot show the figure.')

# -- Project information -----------------------------------------------------

project = 'gamba'
copyright = '2020, Oliver J. Scholten'
author = 'Oliver J. Scholten'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = '0.0.1 beta'


update_time = str(round(time.time()))
print('updated:', update_time)
rst_epilog = ".. |time_badge| image:: https://img.shields.io/date/%s?label=%s&style=for-the-badge&color=brightgreen" % (quote(update_time), quote('Last Updated'))
rst_epilog += "\n.. |version_badge| image:: https://img.shields.io/static/v1?label=%s&message=%s&color=blue&style=for-the-badge" % (quote('Current Release'), quote(release))
rst_epilog += "\n.. |license_badge| image:: https://img.shields.io/static/v1?label=Licence&message=MIT&color=purple&style=for-the-badge"

#'https://img.shields.io/date/%s?label=Last&style=for-the-badge&color=green

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.extlinks',
    'sphinxcontrib.napoleon',
    'sphinx_automodapi.automodapi',
    'sphinx_gallery.gen_gallery',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive'
]
add_module_names = False


sphinx_gallery_conf = {
     'examples_dirs': 'gallery_examples',   # path to your example scripts
     'gallery_dirs': 'gallery',  # path to where to save gallery generated output
     'reference_url': {
         # The module you locally document uses None
        'sphinx_gallery': None,
    },
     'show_memory': True
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# 
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'
master_doc = 'index'

language = 'Python'
exclude_patterns = []
pygments_style = 'sphinx'
html_static_path = ['_static']

html_sidebars = { '**': ['infobox.html', 'searchbox.html'] }

from better import better_theme_path
html_theme_path = [better_theme_path]
html_theme = 'better'

htmlhelp_basename = 'gambadoc'
html_title = 'gamba'
html_short_title = 'gamba'
#html_logo = 'html_resources/logo.svg'

html_theme_options = {}
html_theme_options['cssfiles'] = ['_static/style.css']


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'gamba', 'gamba Documentation',
     [author], 1)
]


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}



# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
man_pages = [
    (master_doc, 'gamba', 'gamba Documentation',
     [author], 1)
]
latex_elements = {
    'extraclassoptions': 'openany'
}