__author__ = 'sevas'

import os.path

LIVE=False

if LIVE:
    JSON_DATABASE_PATH = '/home/www/django-sites/data/csxj_viewer_database'
else:
    JSON_DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'static_data')
