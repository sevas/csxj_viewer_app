from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('provider',
                       url(r'^$', 'befr_news_viewer_app.provider.views.index'),)

