import os

DEBUG = True
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Application specific config
APP_NAME = "Hacker Monthly Finder"
APP_TAGLINE = "Search for articles within your Hacker Montly subscriptions" 

# Location of all hacker montly epub files
HM_EPUB_FILES = os.path.join(PROJECT_ROOT, 'data')

# Elastic search index name
ES_INDEX_NAME = 'hackermonthly'
ES_INDEX_SCHEMA = os.path.join(PROJECT_ROOT, 'schema', 'index.json')

try:
    from settings_local import *
except:
    pass
