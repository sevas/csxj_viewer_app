from django.http import HttpResponse
from django.template import Context, loader

import os, os.path
from jsondb import jsondb
from article import ArticleData
import version

STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')


def load_sidebar_data():
    last_update = jsondb.get_last_status_update(STATIC_DATA_PATH)
    res = {}
    res.update(last_update)
    return res


def load_footer_data():
    return {'version':version.VERSION}


def index(request):

    t = loader.get_template('source_list.html')
    d = {}
    sidebar_data = load_sidebar_data()    
    d.update(sidebar_data)

    source_stats = jsondb.get_per_source_statistics(STATIC_DATA_PATH)
    d.update({'sources':source_stats})

    overall_stats = jsondb.make_overall_statistics(source_stats)
    d.update(overall_stats)

    d.update(load_footer_data())

    c = Context(d)

    return HttpResponse(t.render(c))


def archives(request):
    t = loader.get_template('source_main.html')

    return HttpResponse(t.render({}))


def show_source_summary(request, source_name):
    return HttpResponse(request.path, source_name)
