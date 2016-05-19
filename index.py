#-*- coding:utf-8 -*-
import django
import json
def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)
    body=["Welcome to Baidu Cloud!\n"]
    a=json.dumps({"aaa":"bbb"})
    return a

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
