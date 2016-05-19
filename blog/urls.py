from django.conf.urls import patterns, include, url
from blog import views
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mysite.views.home', name='home'),
                       url(r'^$', views.index),
                       url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail),
                       url(r'^posts/tag/(?P<tag>\w+)$',
                           views.post_list_by_tag, name='list_by_tag'),
                       url(r'^posts/category/(?P<cg>\w+)$',
                           views.post_list_by_category, name='list_by_cg'),
                       url(r'^post/new/$', views.post_new, name='post_new'),
                       url(r'^post/(?P<pk>[0-9]+)/edit/$',
                           views.post_edit, name='post_edit'),
                       url(r'^drafts/$', views.post_draft_list,
                           name='post_draft_list'),
                       url(r'^post/(?P<pk>[0-9]+)/publish/$',
                           views.post_publish, name='post_publish'),
                       url(r'^post/(?P<pk>[0-9]+)/remove/$',
                           views.post_remove, name='post_remove'),

                       url(r'^testblog/$', views.testblog),
                       url(r'^esptemp/$', views.temp),
                       url(r'^testjson/$', views.testjson),
                       )
