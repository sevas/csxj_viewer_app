from django.http import HttpResponse
from django.template import Context, loader

import os, os.path
from datetime import datetime

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
    values = {}
    values.update(base_template.load_sidebar_data(STATIC_DATA_PATH))
    values.update(base_template.load_footer_data())

    available_sources = jsondb.get_source_list(STATIC_DATA_PATH)
    if source_name in available_sources:
        all_days = jsondb.get_all_days(STATIC_DATA_PATH, source_name)

        values.update({'all_days':all_days, 'source_name':source_name})
        t = loader.get_template('source_all_days.html')
        c = Context(values)
        return HttpResponse(t.render(c))
    
    else:
        t = loader.get_template('source_day_not_found.html')
        values.update({'reason':'There is no content provider with that id : {0}'.format(source_name)})
        c = Context(values)
        return HttpResponse(t.render(c))









def find_next_and_prev_days(current_day, available_days):
    idx = available_days.index(current_day)
    num_days = len(available_days)

    if num_days == 1:
        prev_day, next_day = None, None
    elif num_days == 2:
        if idx == 0:
           prev_day = None
           next_day = available_days[1]
        else:
               prev_day = available_days[0]
               next_day = None
    else:
        if idx == 0:
            prev_day = None
            next_day = available_days[1]
        elif idx == (num_days - 1):
            prev_day = available_days[idx-1]
            next_day = None
        else:
            prev_day = available_days[idx-1]
            next_day = available_days[idx+1]

    return prev_day, next_day


def show_source_day_summary(request, source_name, year, month, day):
    y, m, d = [int(i) for i in (year, month, day)]
    values = {}
    values.update(base_template.load_sidebar_data(STATIC_DATA_PATH))
    values.update(base_template.load_footer_data())

    available_sources = jsondb.get_source_list(STATIC_DATA_PATH)
    if source_name in available_sources:
        date_string = '{0}-{1}-{2}'.format(year, month, day)
        available_days = jsondb.get_all_days(STATIC_DATA_PATH, source_name)
        if date_string in available_days:
            prev_day, next_day = find_next_and_prev_days(date_string, available_days)
            articles_per_batch = jsondb.get_articles_per_batch(STATIC_DATA_PATH, source_name, date_string)

            values.update({'current_date':datetime(y, m, d),
                           'prev_day':prev_day,
                           'next_day':next_day,
                           'articles_per_batch':articles_per_batch,
                           'source_name':source_name
                          })

            c = Context(values)
            t = loader.get_template('source_day.html')
            return HttpResponse(t.render(c))
            
        else:
            # render invalid date
            t = loader.get_template('source_day_not_found.html')
            c = Context(values)
            values.update({'reason':'There is no data to show you for that date : ' + datetime(y,m,d).strftime('%B %d, %Y')})
            return HttpResponse(t.render(c))
    else:
        # render invalid source
        t = loader.get_template('source_day_not_found.html')
        values.update({'reason':'There is no content provider with that id : {0}'.format(source_name)})
        c = Context(values)
        return HttpResponse(t.render(c))



def show_source_day_batch_summary(request, source_name, year, month, day, time):
    return HttpResponse('day batch summary : '+source_name+year+month+day+time)
