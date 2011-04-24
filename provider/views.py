from django.http import HttpResponse
from django.template import Context, loader

import os, os.path
from jsondb import jsondb
from article import ArticleData

STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')


def load_sidebar_data():
    overall_stats = jsondb.get_overall_statistics(STATIC_DATA_PATH)
    last_update = jsondb.get_last_status_update(STATIC_DATA_PATH)

    res = {}
    res.update(overall_stats)
    res.update(last_update)
    return res



def index(request):
    sources = jsondb.get_subdirectories(STATIC_DATA_PATH)
    t = loader.get_template('source_list.html')

    d = {'sources':sources}
    sidebar_data = load_sidebar_data()    
    d.update(sidebar_data)

    c = Context(d)

    return HttpResponse(t.render(c))


def archives(request):
    t = loader.get_template('source_main.html')

    return HttpResponse(t.render({}))


def show_source_summary(request, source_name):
    return HttpResponse(request.path, source_name)
