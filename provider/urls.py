from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^(.*)/(\d\d\d\d)-(\d\d)-(\d\d)/(\d\d).(\d\d).(\d\d)$', 'provider.views.show_source_day_batch_summary'),
                       url(r'^(.*)/(\d\d\d\d)-(\d\d)-(\d\d)$', 'provider.views.show_source_day_summary'),
                       url(r'^(.+)$', 'provider.views.show_source_summary'),
                       url(r'^$', 'provider.views.index'),)


