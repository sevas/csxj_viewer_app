from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^404/', 'befr_news_viewer_app.errors.views.custom_404'),
    url(r'^source/', include('befr_news_viewer_app.provider.urls')),
    url(r'^$', 'befr_news_viewer_app.summary.views.index'),

    # url(r'^befr_news_viewer_app/', include('befr_news_viewer_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

