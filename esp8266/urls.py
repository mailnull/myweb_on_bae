from django.conf.urls import patterns, include, url
from dwebsocket.decorators import accept_websocket, require_websocket
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from esp8266 import views


def base_view(request):
    return render_to_response('base_restfull.html', {}, context_instance=RequestContext(request))

clients = []


#@accept_websockets
@require_websocket
def echo(request):
    if request.is_websocket:
        try:
            clients.append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                for client in clients:
                    client.send(message)
        finally:
            clients.remove(request.websocket)


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'mysite.views.home', name='home'),
                       url(r'^$', views.index, name='espindex'),
                       url(r'^device/(?P<device>\w+)$',
                           views.list_by_device, name="list_by_device"),
                       url(r'^return_xml/$', views.return_xml),
                       url(r'^file/$', views.fileupdate),
                       url(r'^jsontest/$', views.jsontest),
                       url(r'^base/$', base_view),
                       url(r'^echo/$', echo, name='espsocket'),
                       url(r'^modform/$', views.modform),

                       )
