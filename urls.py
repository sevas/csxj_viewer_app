from django.conf.urls import patterns, include, url
from feeds.queueerrorsfeed import LatestEntriesFeed

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',

    url(r'^source/', include('provider.urls')),
    url(r'^feed/queueerrors/$', LatestEntriesFeed),
    url(r'^$', 'summary.views.index'),

)

