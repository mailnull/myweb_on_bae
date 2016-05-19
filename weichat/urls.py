from django.conf.urls import patterns, url
from weichat import views
#from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'msg', views.MsgViewSet)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mysite.views.home', name='home'),
                       url(r'^$', views.index),
                       url(r'^weichat/$', views.weichatbase),
                       url(r'^websocket/$', views.websocket_base, name='websocket'),
                       url(r'^echo/$', views.websocket_echo),
                       #  url(r'^api/', include(router.urls)),
                       # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                       )
