from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'provider.views.index'),
                       url(r'(.*)$', 'provider.views.show_source_summary'))

