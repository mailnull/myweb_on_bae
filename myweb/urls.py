from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
#from django.core.cache import cache

from django.shortcuts import render_to_response
from django.conf import settings


def testredis(request):
    import os
    if 'SERVER_SOFTWARE' in os.environ:

        import redis
        db_name = "ZuriHfOCGBOrvQjfMlZJ"
        api_key = "dce9b62692b7446391f52cca2840784e"
        secret_key = "86558724fa9d48ab91a5283a2bb3d061"
        myauth = "%s-%s-%s" % (api_key, secret_key, db_name)
        r = redis.Redis(host="redis.duapp.com", port=80, password=myauth)
        if r.hexists('testhset', 'testredis'):
            r.hset('testhset', 'testredis', "this is test bae redis_cache")
            h = r.hget('testhset', 'testredis')
        if r.exists('test'):
            r.delete('test')
    else:
        con = get_redis_connection("default")
        con.hset('test', 'testredis', "this is test bae redis_cache")
        h = con.hget('test', 'testredis')
    import json
    return HttpResponse(json.dumps({'test': h}))


@csrf_exempt
def testreq(req):
    response = None
    if req.method == "GET":
        from django.template import Context, Template
        t = Template("<p>pk={{ pk }}</p>")
        c = Context({'pk': req.GET.get("pk", '')})
        return HttpResponse(t.render(c))
    elif req.method == "POST":
        response = req.body
    return HttpResponse(response or None)

# flag=1
# clients=[]
# def modify_message(message):
#   return message.lower()


# @csrf_exempt
# def testpost(request):
#     if request.method =="POST":
#         return HttpResponse(request.POST.items())
#     return HttpResponse(request.GET.items())

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'myweb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # url(r'^testpost/$',testpost),
                       #url(r'^testtedis/$', testredis),

                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'login.html'}),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                           {'next_page': '/blog/'}),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^blog/', include('blog.urls')),
                       url(r'^weichat/', include('weichat.urls')),

                       url(r'^snippet/', include('snippets.urls')),

                       url(r'^myhome/', include('myhome.urls')),
                       url(r'^testreq/$', testreq, name='testreq'),

                       # url(r'^testjson/$',testjson),


                       url(r'^esp8266/', include('esp8266.urls')),

                       )
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}),
                            )
