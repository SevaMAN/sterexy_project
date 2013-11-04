from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from sterexy_project import settings


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^$', 'sterexy.views.index', name='index'),
)
