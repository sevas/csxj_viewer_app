__author__ = 'sevas'

import os, os.path
from datetime import time, datetime
from itertools import chain
import json
from article import ArticleData

from providerstats import ProviderStats


def get_subdirectories(parent_dir):
    """
    Yields a list of directory names. Filter out anything that is not a directory
    """
    return [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]


def get_source_list(db_root):
    return get_subdirectories(db_root)


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


def get_provider_dump(filename):
    with open(filename, 'r') as f:
        json_content = f.read()
        return json.loads(json_content)



def get_latest_fetched_articles(db_root):
    providers = get_subdirectories(db_root)

    last_articles = {}
    last_errors = {}

    # todo: fix that shit
    fetched_date = datetime.today().date()

    for p in providers:
        provider_dir = os.path.join(db_root, p)
        all_days = get_subdirectories(provider_dir)
        last_day = get_latest_day(all_days)

        last_day_dir = os.path.join(provider_dir, last_day)
        all_hours = get_subdirectories(last_day_dir)
        last_hour = get_latest_hour(all_hours)

        fetched_date = make_date_from_string(last_day, last_hour)

        filename = os.path.join(last_day_dir, last_hour, 'articles.json')

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


def get_last_status_update(db_root):
    fetched_date, articles, errors = get_latest_fetched_articles(db_root)

    stats = collect_stats(articles, errors)
    stats.update({'update_date':fetched_date[0].strftime('%B %d, %Y'),
                 'update_time':fetched_date[1].strftime('%H:%M')})

    return stats 
    


def get_overall_statistics(db_root):
    providers = get_subdirectories(db_root)

    overall_stats = {'total_articles':0, 'total_errors':0, 'total_links':0, 'start_date':None, 'end_date':None}
    for p in providers:
        stats_filename = os.path.join(db_root, p, 'stats.json')
        provider_stats = ProviderStats.load_from_file(stats_filename)

        overall_stats['total_articles'] += provider_stats.n_articles
        overall_stats['total_errors'] += provider_stats.n_errors
        overall_stats['total_links'] += provider_stats.n_links
        overall_stats['start_date'] = provider_stats.start_date
        overall_stats['end_date'] = provider_stats.end_date

    return overall_stats


def make_overall_statistics(source_statistics):
    overall_stats = {'total_articles':0, 'total_errors':0, 'total_links':0, 'start_date':None, 'end_date':None}
    for (name, provider_stats) in source_statistics.items():
        overall_stats['total_articles'] += provider_stats.n_articles
        overall_stats['total_errors'] += provider_stats.n_errors
        overall_stats['total_links'] += provider_stats.n_links
        overall_stats['start_date'] = provider_stats.start_date
        overall_stats['end_date'] = provider_stats.end_date

    return overall_stats


def get_per_source_statistics(db_root):
    sources = get_subdirectories(db_root)

    source_stats = {}
    for source_name in sources:
        stats_filename = os.path.join(db_root, source_name, 'stats.json')
        source_stats[source_name] = ProviderStats.load_from_file(stats_filename)

    return source_stats


def get_all_days(db_root, source_name):
    all_days = get_subdirectories(os.path.join(db_root, source_name))
    all_days.sort()
    return all_days


def get_articles_per_batch(db_root, source_name, date_string):
    path = os.path.join(db_root, source_name, date_string)

    all_batch_times = os.listdir(path)
    all_batches = []
    for batch_time in all_batch_times:
        json_file = os.path.join(path, batch_time, 'articles.json')
        with open(json_file, 'r') as f:
            json_content = json.load(f)
            articles = [ArticleData.from_json(json_string) for json_string in json_content['articles']]
            all_batches.append((batch_time, articles))

    all_batches.sort(key=lambda x: x[0])
    return all_batches