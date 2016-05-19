from django.conf.urls import patterns, include, url
from myhome import views

urlpatterns = patterns('',
                       url(r'^display_log/$',
                           views.display_log, {'pk': None}, name='display_log'),
                       url(r'^display_log/(?P<pk>[0-9]+)/$',
                           views.display_log, name='display_log'),
                       )
