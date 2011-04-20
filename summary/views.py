# Create your views here.
import sys
sys.path.append('dependencies')
import os, os.path
import json
from datetime import datetime, time
from django.http import HttpResponse
from django.template import Context, loader

import logging
logger = logging.getLogger(__name__)

from article import ArticleData



def make_time(time_string):
    h, m, s = [int(i) for i in time_string.split('.')]
    return time(h, m ,s)


def get_latest_hour(hour_directory_names):
    """
    """
    l = [(make_time(time_string), time_string) for time_string in hour_directory_names]
    return max(l, key=lambda x: x[0])[1]


def make_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')


def get_latest_day(day_directory_names):
    """
    """
    l = [(make_date(date_string), date_string) for date_string in day_directory_names]
    last_day = max(l, key=lambda x: x[0])[1]
    return last_day



def get_latest_fetched_articles():
    path = 'static_data'
    providers = os.listdir(path)

    last_articles = {}

    for p in providers:
        all_days = [d for d in os.listdir(os.path.join(path, p)) if not d.endswith('json')]
        last_day = get_latest_day(all_days)
        all_hours = os.listdir(os.path.join(path, p, last_day))
        last_hour = get_latest_hour(all_hours)

        filename = os.path.join(path, p, last_day, last_hour, 'articles.json')
        with open(filename, 'r') as f:
            json_content = f.read()
            dump = json.loads(json_content)

            articles = []
            for article in dump['articles']:
                articles.append(ArticleData.from_json(article))

            last_articles[p] = articles
            
    return last_articles


def index(request):
    t = loader.get_template('summary.html')

    articles = get_latest_fetched_articles()

    c = Context({'all_articles':articles})

    return HttpResponse(t.render(c))