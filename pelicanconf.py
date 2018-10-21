#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Evidlo'
AUTHOR = 'SINE'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "./themes/crowsfoot"
PROFILE_IMAGE_URL="https://marcel.nlogn.org/profile.jpg"
SITESUBTITLE = "The official page of Signals, Inference and Networks Group at UIUC"

MENUITEMS = (('Blog', '/blog/'),
             ('Calendar', '/calendar'),
             )


GITHUB_ADDRESS = 'http://github.com/uiuc-sine'
PLUGINS = ["render_math"]
PLUGIN_PATHS = ['./plugins']
