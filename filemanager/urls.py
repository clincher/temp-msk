from django.conf.urls.defaults import *
urlpatterns = patterns('filemanager.adminviews',
    (r'^popup/$', 'popap'),
    (r'^filemanager/$', 'index'),
)
