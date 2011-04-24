from django.http import HttpResponse
from django.template import Context, loader

import os, os.path
from jsondb import jsondb
from article import ArticleData
from common import base_template

STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')

def index(request):

    t = loader.get_template('source_list.html')
    d = {}
    sidebar_data =  base_template.load_sidebar_data(STATIC_DATA_PATH)
    d.update(sidebar_data)

    source_stats = jsondb.get_per_source_statistics(STATIC_DATA_PATH)
    d.update({'sources':source_stats})

    overall_stats = jsondb.make_overall_statistics(source_stats)
    d.update(overall_stats)

    d.update(base_template.load_footer_data())

    c = Context(d)

    return HttpResponse(t.render(c))


def archives(request):
    t = loader.get_template('source_main.html')

    return HttpResponse(t.render({}))


def show_source_summary(request, source_name):
    return HttpResponse(request.path, source_name)
