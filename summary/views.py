# Create your views here.

import os.path
from django.http import HttpResponse
from django.template import Context, loader

import csxj.db as csxjdb

from common import base_template


STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')



def index(request):
    t = loader.get_template('summary.html')

    fetched_date, articles, errors = csxjdb.get_latest_fetched_articles(STATIC_DATA_PATH)

    template_values = {'all_articles':articles}
    template_values.update(base_template.load_sidebar_data(STATIC_DATA_PATH))
    template_values.update(base_template.load_footer_data())
    template_values.update(base_template.load_queued_items_count(STATIC_DATA_PATH))
    c = Context(template_values)

    return HttpResponse(t.render(c))