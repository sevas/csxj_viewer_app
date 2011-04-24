# Create your views here.

import os.path
from django.http import HttpResponse
from django.template import Context, loader

from jsondb import jsondb
from article import ArticleData
from providerstats import ProviderStats
from common import base_template


STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')



def index(request):
    t = loader.get_template('summary.html')

    fetched_date, articles, errors = jsondb.get_latest_fetched_articles(STATIC_DATA_PATH)

    template_values = {'all_articles':articles}
    template_values.update(base_template.load_sidebar_data(STATIC_DATA_PATH))
    template_values.update(base_template.load_footer_data())
    c = Context(template_values)

    return HttpResponse(t.render(c))