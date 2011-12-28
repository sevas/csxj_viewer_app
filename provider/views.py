import os, os.path
from datetime import datetime

from django.http import HttpResponse
from django.template import Context, loader

import csxj.db as csxjdb

from common import base_template

STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')

def index(request):
    t = loader.get_template('source_list.html')
    d = {}
    sidebar_data =  base_template.load_sidebar_data(STATIC_DATA_PATH)
    d.update(sidebar_data)

    stats_by_source= csxjdb.get_per_source_statistics(STATIC_DATA_PATH)
    overall_stats = csxjdb.make_overall_statistics(stats_by_source)
    d.update(overall_stats)


    sources_data = dict()
    for source_name, stats in stats_by_source.items():
        p = csxjdb.Provider(STATIC_DATA_PATH, source_name)
        sources_data[source_name] = (stats, p.get_queued_items_count())

    d.update({'sources_data':sources_data})
    d.update(base_template.load_footer_data())

    c = Context(d)

    return HttpResponse(t.render(c))


def render_not_found(reason):
    values = base_template.load_all_common_values(STATIC_DATA_PATH)
    
    t = loader.get_template('source_day_not_found.html')
    values.update(dict(reason=reason))
    c = Context(values)
    return HttpResponse(t.render(c))



def show_source_summary(request, source_name):

    available_sources = csxjdb.get_all_provider_names(STATIC_DATA_PATH)
    if source_name in available_sources:
        p = csxjdb.Provider(STATIC_DATA_PATH, source_name)
        values = base_template.load_all_common_values(STATIC_DATA_PATH)

        all_days = p.get_source_summary_for_all_days()
        
        values.update({'all_days':all_days, 'source_name':source_name})
        t = loader.get_template('source_all_days.html')
        c = Context(values)

        return HttpResponse(t.render(c))
    else:
        return render_not_found('There is no content provider with that id : {0}'.format(source_name))




def find_next_and_prev_days(current_day, available_days):
    """
    From the directory list ('YYYY-MM-DD'), find the next a previous days available,
    to generate the 'Previous Day' and 'Next Day' links.

    current_day is a 'YYYY-MM-DD' string, and is expected to exist.
    available_days is a sorted list of 'YYYY-MM-DD' strings,
    """
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
    """
    Renders the summary for one day of crawling.
    Shows a list of all articles downloaded that day, grouped by 'batch'
    """
    y, m, d = [int(i) for i in (year, month, day)]


    available_sources = csxjdb.get_all_provider_names(STATIC_DATA_PATH)
    if source_name in available_sources:
        p = csxjdb.Provider(STATIC_DATA_PATH, source_name)
        date_string = '{0}-{1}-{2}'.format(year, month, day)
        available_days = p.get_all_days()
        if date_string in available_days:
            values = base_template.load_all_common_values(STATIC_DATA_PATH)

            prev_day, next_day = find_next_and_prev_days(date_string, available_days)
            articles_and_errorcounts_per_batch = p.get_articles_and_errorcounts_per_batch(date_string)

            values.update({'current_date':datetime(y, m, d),
                           'prev_day':prev_day,
                           'next_day':next_day,
                           'articles_per_batch':articles_and_errorcounts_per_batch,
                           'source_name':source_name,
                           'error_count':sum([err for (day, art, err) in articles_and_errorcounts_per_batch])
                          })

            c = Context(values)
            t = loader.get_template('source_day.html')
            return HttpResponse(t.render(c))
        else:
            return render_not_found('There is no data to show you for that date : ' + datetime(y,m,d).strftime('%B %d, %Y'))
    else:
        return render_not_found('There is no content provider with that id : {0}'.format(source_name))



def show_source_day_batch_articles(request, source_name, year, month, day, hours, minutes, seconds):
    """
    Renders the summary for one day of crawling.
    Shows a list of all articles downloaded that day, grouped by 'batch'
    """
    def get_values_for_batch_articles(provider, date_string, batch_hour_string):
        articles, error_count = provider.get_batch_content(date_string, batch_hour_string)
        return {'articles':articles,
                'source_name':source_name,
                'error_count':error_count,
                'batch_url':"/source/{0}/{1}/{2}".format(source_name, date_string, batch_hour_string)}

    return render_batch_data(source_name, year, month, day, hours, minutes, seconds, 'source_batch.html', get_values_for_batch_articles)




def show_source_day_batch_errors(request, source_name, year, month, day, hours, minutes, seconds):
    """

    """
    def get_values_for_batch_errors(provider, date_string, batch_hour_string):
        errors = provider.get_errors_from_batch(date_string, batch_hour_string)
        return {'errors':errors,
                'source_name':source_name,
                'batch_url':"/source/{0}/{1}/{2}".format(source_name, date_string, batch_hour_string)}

    return render_batch_data(source_name, year, month, day, hours, minutes, seconds, 'source_batch_errors.html', get_values_for_batch_errors)




def render_batch_data(source_name, year, month, day, hours, minutes, seconds, template_filename, get_template_values_fn):
    y, m, d = [int(i) for i in (year, month, day)]
    h, mm, s = [int(i) for i in (hours, minutes, seconds)]

    available_sources = csxjdb.get_all_provider_names(STATIC_DATA_PATH)
    if source_name in available_sources:
        p = csxjdb.Provider(STATIC_DATA_PATH, source_name)
        date_string = '{0}-{1}-{2}'.format(year, month, day)
        available_days = p.get_all_days()
        if date_string in available_days:
            available_batches = p.get_all_batch_hours(date_string)
            batch_string = '{0}.{1}.{2}'.format(hours, minutes, seconds)
            
            if batch_string in available_batches:
                values = base_template.load_all_common_values(STATIC_DATA_PATH)
            
                values.update(get_template_values_fn(p, date_string, batch_string))
                
                t = loader.get_template(template_filename)
                c = Context(values)
                return HttpResponse(t.render(c))

            else:
                return render_not_found('This source has no data to show you for that date and time : ' + asked_datetime.strftime('%B %d, %Y at %H:%M:%S'))
        else:
            return render_not_found('There is no data to show you for that date : ' + datetime(y,m,d).strftime('%B %d, %Y'))
    else:
        return render_not_found('There is no content provider with that id : {0}'.format(source_name))
    





def show_source_graphs(request, source_name):
    available_sources = csxjdb.get_all_provider_names(STATIC_DATA_PATH)
    if source_name in available_sources:
        values = base_template.load_all_common_values(STATIC_DATA_PATH)
        values.update({'source_name':source_name})

        t = loader.get_template('source_graphs.html')
        c = Context(values)
        return HttpResponse(t.render(c))
    else:
        return render_not_found('There is no content provider with that id : {0}'.format(source_name))




def show_download_queue(request, source_name):
    available_sources = csxjdb.get_all_provider_names(STATIC_DATA_PATH)
    if source_name in available_sources:
        values = base_template.load_all_common_values(STATIC_DATA_PATH)

        p = csxjdb.Provider(STATIC_DATA_PATH, source_name)
        download_queue = p.get_queued_batches_by_day()
        values.update({'queued_items_by_day':download_queue,
                       'source_name':source_name})
        c = Context(values)
        t = loader.get_template('download_queue.html')
        return HttpResponse(t.render(c))
    else:
        return render_not_found('There is no content provider with that id : {0}'.format(source_name))
