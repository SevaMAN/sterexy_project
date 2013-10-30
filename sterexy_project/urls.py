from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'sterexy.views.index', name='index'),
)
