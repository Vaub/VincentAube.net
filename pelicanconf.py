#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Vincent Aub\xe9'
SITENAME = u'VincentAube.net'
EMAIL = 'vincent.aube@hotmail.com'
SITEURL = ''

PATH = 'content'
THEME = 'theme'
INDEX_SAVE_AS = 'blog_index.html'

TIMEZONE = 'America/Montreal'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

MENUITEMS = (
    ('Projets', '/pages/projects.html'),
    ('Blog', '/blog_index.html'),
    ('À propos', '/pages/about.html'),
)

EXTRA_PATHS = ["extra/{}".format(f) for f in os.listdir('content/extra/')]

STATIC_PATHS = ['images'] + EXTRA_PATHS
EXTRA_PATH_METADATA = {f: {'path': os.path.basename(f)} for f in EXTRA_PATHS}

# Blogroll
LINKS = ()
        #(('Pelican', 'http://getpelican.com/'),
        # ('Python.org', 'http://python.org/'),
        # ('Jinja2', 'http://jinja.pocoo.org/'),
        # ('You can modify those links in your config file', '#'),)



# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/vaub0039'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
