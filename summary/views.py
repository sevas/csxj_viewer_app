# Create your views here.

import os.path
from django.http import HttpResponse
from django.template import Context, loader

from jsondb import jsondb
from article import ArticleData
from providerstats import ProviderStats
import version



def load_footer_data():
    return {'version':version.VERSION}


STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')



def load_sidebar_data():
    overall_stats = jsondb.get_overall_statistics(STATIC_DATA_PATH)
    last_update = jsondb.get_last_status_update(STATIC_DATA_PATH)

    res = {}
    res.update(overall_stats)
    res.update(last_update)
    return res



def index(request):
    t = loader.get_template('summary.html')

    fetched_date, articles, errors = jsondb.get_latest_fetched_articles(STATIC_DATA_PATH)

    template_values = {'all_articles':articles}
    template_values.update(load_sidebar_data())
    template_values.update(load_footer_data())
    c = Context(template_values)

    return HttpResponse(t.render(c))