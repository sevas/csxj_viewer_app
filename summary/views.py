# Create your views here.

import os.path
from django.http import HttpResponse
from django.template import Context, loader

import csxj.db as csxjdb

from common import base_template


STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')



def index(request):
    t = loader.get_template('summary.html')

    last_update = csxjdb.get_summary_from_last_update_for_all_sources(STATIC_DATA_PATH)

    summary_per_source = list()

    for name, date, metainfo in last_update:
        url = "/source/{0}/{1}".format(name, csxjdb.utils.convert_date_to_string(date))
        summary_per_source.append((name, date, metainfo, url))

    template_values = {'summary_per_source':summary_per_source}
    template_values.update(base_template.load_sidebar_data(STATIC_DATA_PATH))
    template_values.update(base_template.load_footer_data())
    template_values.update(base_template.load_queued_items_count(STATIC_DATA_PATH))
    c = Context(template_values)

    return HttpResponse(t.render(c))