# Create your views here.
import sys
sys.path.append('dependencies')
import os, os.path
import json
from datetime import datetime, time, date
from django.http import HttpResponse
from django.template import Context, loader
from itertools import chain

import logging
logger = logging.getLogger(__name__)

from article import ArticleData
from providerstats import ProviderStats


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


def make_date_from_string(date_string, time_string):
    return make_date(date_string), make_time(time_string)


def get_statistics():
    path = 'static_data'
    providers = os.listdir(path)

    overall_stats = {'total_articles':0, 'total_errors':0, 'total_links':0, 'start_date':None, 'end_date':None}
    for p in providers:
        stats_filename = os.path.join(path, p, 'stats.json')
        provider_stats = ProviderStats.load_from_file(stats_filename)

        overall_stats['total_articles'] += provider_stats.n_articles
        overall_stats['total_errors'] += provider_stats.n_errors
        overall_stats['total_links'] += provider_stats.n_links
        overall_stats['start_date'] = provider_stats.start_date
        overall_stats['end_date'] = provider_stats.end_date

    return overall_stats


def get_provider_dump(filename):
    with open(filename, 'r') as f:
        json_content = f.read()
        return json.loads(json_content)

def get_latest_fetched_articles():
    path = 'static_data'
    providers = os.listdir(path)

    last_articles = {}
    last_errors = {}

    for p in providers:
        all_days = [d for d in os.listdir(os.path.join(path, p)) if not d.endswith('json')]
        last_day = get_latest_day(all_days)
        all_hours = os.listdir(os.path.join(path, p, last_day))
        last_hour = get_latest_hour(all_hours)

        fetched_date = make_date_from_string(last_day, last_hour)

        filename = os.path.join(path, p, last_day, last_hour, 'articles.json')

        dump = get_provider_dump(filename)

        articles, errors = [], []
        for article in dump['articles']:
            articles.append(ArticleData.from_json(article))

        for error in dump['errors']:
            errors.append(error)

        last_articles[p] = articles
        last_errors[p] = errors

    return fetched_date, last_articles, last_errors


def collect_stats(all_articles, all_errors):
    num_providers = len(all_articles.keys())
    num_articles =  sum(len(articles) for articles in chain(all_articles.values()))
    num_errors = sum(len(errors) for errors in chain(all_errors.values()))

    return {'num_providers':num_providers, 'num_articles':num_articles, 'num_errors':num_errors}

def index(request):
    t = loader.get_template('summary.html')

    fetched_date, articles, errors = get_latest_fetched_articles()
    stats = collect_stats(articles, errors)
    stats.update({'update_date':fetched_date[0].strftime('%B %d, %Y'),
                 'update_time':fetched_date[1].strftime('%H:%M')})

    template_values = {'all_articles':articles}
    template_values.update(stats)

    overall_stats = get_statistics()
    template_values.update(overall_stats)

    c = Context(template_values)

    return HttpResponse(t.render(c))