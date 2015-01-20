# -*- coding: utf-8 -*-

import time

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]
source_suffix = '.rst'
master_doc = 'index'
project = u'satbot'
copyright = u'{0}, Mike Burr <mburr@unintuitive.org>'.format(time.localtime().tm_year)
version = open('../VERSION', 'r').read().strip()
release = version
exclude_patterns = ['_build']
pygments_style = 'sphinx'
htmlhelp_basename = 'satbot'
