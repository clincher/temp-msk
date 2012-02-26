from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^dirlist/$', 'filemanager.connector.views.dirlist'),
    (r'^$', 'filemanager.connector.views.handler'),
)
