from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(.*)/(\d\d\d\d)-(\d\d)-(\d\d)/(\d\d).(\d\d).(\d\d)/articles$', 'provider.views.show_source_day_batch_articles'),
    url(r'^(.*)/(\d\d\d\d)-(\d\d)-(\d\d)/(\d\d).(\d\d).(\d\d)/errors$', 'provider.views.show_source_day_batch_errors'),
    url(r'^(.*)/(\d\d\d\d)-(\d\d)-(\d\d)$', 'provider.views.show_source_day_summary'),
    url(r'^(.*)/graphs$', 'provider.views.show_source_graphs'),
    url(r'^(.*)/queue$', 'provider.views.show_download_queue'),
    url(r'^(.+)$', 'provider.views.show_source_summary'),
    url(r'^$', 'provider.views.index'),)
